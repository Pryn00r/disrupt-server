# online_server.py
# Iteration 37: the online server. Every copy of Disrupt connects to this one program, which:
#   - signs players in (the same username and password as in the game),
#   - knows who is online, so a username can be searched for,
#   - passes challenges between players and starts the battle when one is accepted,
#   - runs every online battle itself (online_engine.Match), so nobody can cheat,
#   - keeps ratings and the battle history in the database (online_db.py).
# It talks to the games with WebSockets: a connection that stays open, so the server can send a message
# (like "Simran challenges you!") the moment it happens. Every message is a small piece of JSON with a 'type'.
#
# Run on my computer:   python online_server.py          (then the game connects to ws://localhost:8765)
# On Render it is started the same way; PORT and DATABASE_URL come from Render's settings.

import asyncio
import hashlib
import hmac
import json
import logging
import os
import secrets
import time
import uuid
from http import HTTPStatus

from websockets.asyncio.server import serve
from websockets.exceptions import ConnectionClosed

import online_engine as engine
from online_db import Database
from save_system import validate_username

PROTOCOL = 1                                                   # the game and server must agree on this
TURN_SECONDS = float(os.environ.get('TURN_SECONDS', 60))       # time to choose an action before defending automatically
CHALLENGE_SECONDS = float(os.environ.get('CHALLENGE_SECONDS', 30))
RECONNECT_SECONDS = float(os.environ.get('RECONNECT_SECONDS', 60))   # a player who drops out has this long to come back
MAX_MESSAGE = 64 * 1024                                        # bytes - anything bigger is not a real game message
MAX_FAILED_SIGN_INS = 5
LOCKOUT_SECONDS = 300

log = logging.getLogger('disrupt')


def hash_secret(text, salt):
	return hashlib.pbkdf2_hmac('sha256', text.encode('utf-8'), salt.encode('utf-8'), 100_000).hex()


class Player:
	def __init__(self, connection, user):
		self.connection = connection
		self.key = user['key']
		self.name = user['username']
		self.room = None


class Room:
	def __init__(self, server, keys, names, format_name, rule, teams_sent):
		self.server = server
		self.id = uuid.uuid4().hex[:12]
		self.keys = keys                # {'a': key, 'b': key}
		self.names = names
		self.format = format_name
		self.rule = rule
		self.teams_sent = teams_sent    # what each player sent (kept for a rematch)
		self.match = None
		self.deadline = None
		self.ended = False
		self.result = None
		self.rematch = set()
		self.gone = {}                  # side -> time the player disconnected

	def side_of(self, key):
		return next(side for side, k in self.keys.items() if k == key)


class Server:
	def __init__(self, database):
		self.db = database
		self.players = {}       # username key -> Player (only players who are online)
		self.challenges = {}    # id -> challenge details
		self.rooms = {}         # id -> Room
		self.failed = {}        # username key -> (failed sign ins, time of the last one)

	# ---------- sending ----------
	async def send(self, key, message):
		player = self.players.get(key)
		if player is None:
			return
		try:
			await player.connection.send(json.dumps(message))
		except ConnectionClosed:
			pass

	async def error(self, connection, code, **extra):
		try:
			await connection.send(json.dumps({'type': 'error', 'code': code, **extra}))
		except ConnectionClosed:
			pass

	# ---------- one connection ----------
	async def handle(self, connection):
		player = None
		try:
			async for raw in connection:
				if len(raw) > MAX_MESSAGE:
					continue
				try:
					message = json.loads(raw)
				except ValueError:
					continue
				if not isinstance(message, dict) or not isinstance(message.get('type'), str):
					continue
				if player is None:
					if message['type'] == 'hello':
						player = await self.sign_in(connection, message)
					else:
						await self.error(connection, 'sign_in_first')
					continue
				handler = getattr(self, 'on_' + message['type'], None)
				if handler is None:
					await self.error(connection, 'unknown_message')
					continue
				try:
					await handler(player, message)
				except (KeyError, TypeError, ValueError) as problem:   # a badly formed message must never stop the server
					log.warning('bad %s from %s: %s', message['type'], player.name, problem)
					await self.error(connection, 'bad_message')
		except ConnectionClosed:
			pass
		finally:
			if player is not None and self.players.get(player.key) is player:
				await self.disconnected(player)

	# ---------- signing in ----------
	# The first time a username goes online it is registered with the player's password. After that the
	# password (or the token the server gave last time) must match. The game stores the token, so the
	# player does not type their password every time.
	async def sign_in(self, connection, message):
		if message.get('version') != PROTOCOL:
			await self.error(connection, 'old_version')
			return None
		username = str(message.get('username', '')).strip()
		key = username.casefold()
		if validate_username(username, []):
			await self.error(connection, 'bad_username')
			return None
		count, last = self.failed.get(key, (0, 0))
		if count >= MAX_FAILED_SIGN_INS and time.time() - last < LOCKOUT_SECONDS:
			await self.error(connection, 'locked')
			return None
		user = self.db.get_user(key)
		password, token = message.get('password'), message.get('token')
		if user is None:
			if not isinstance(password, str) or not 8 <= len(password) <= 64:
				await self.error(connection, 'needs_password')
				return None
			salt = secrets.token_hex(16)
			self.db.create_user(key, username, salt, hash_secret(password, salt))
			user = self.db.get_user(key)
		else:
			good = False
			if isinstance(token, str) and user['token_hash']:
				good = hmac.compare_digest(user['token_hash'], hash_secret(token, user['salt']))
			elif isinstance(password, str):
				good = hmac.compare_digest(user['password_hash'], hash_secret(password, user['salt']))
			if not good:
				self.failed[key] = (count + 1, time.time())
				await self.error(connection, 'token_expired' if token and not password else 'name_taken')
				return None
		self.failed.pop(key, None)
		new_token = secrets.token_hex(32)
		self.db.set_token(key, hash_secret(new_token, user['salt']))

		old = self.players.get(key)   # signed in somewhere else - that connection is closed
		if old is not None:
			await self.error(old.connection, 'signed_in_elsewhere')
			await old.connection.close()
		player = Player(connection, user)
		self.players[key] = player
		await connection.send(json.dumps({'type': 'welcome', 'username': user['username'], 'token': new_token,
		                                  'rating': user['rating'], 'wins': user['wins'], 'losses': user['losses']}))
		# back in a battle that was still going when they dropped out
		for room in self.rooms.values():
			if key in room.keys.values() and not room.ended:
				player.room = room
				room.gone.pop(room.side_of(key), None)
				await self.send_start(room, room.side_of(key), resume = True)
		return player

	async def disconnected(self, player):
		del self.players[player.key]
		for challenge_id, challenge in list(self.challenges.items()):
			if player.key in (challenge['from'], challenge['to']):
				del self.challenges[challenge_id]
				other = challenge['to'] if challenge['from'] == player.key else challenge['from']
				await self.send(other, {'type': 'challenge_cancelled', 'id': challenge_id})
		room = player.room
		if room is not None:
			side = room.side_of(player.key)
			if room.ended:
				await self.leave_room(room, side)
			else:
				room.gone[side] = time.time()
				await self.send(room.keys[engine.other(side)], {'type': 'opponent_left', 'seconds': RECONNECT_SECONDS})

	# ---------- searching and challenging ----------
	async def on_search(self, player, message):
		key = str(message['username']).strip().casefold()
		user = self.db.get_user(key)
		online = self.players.get(key)
		await player.connection.send(json.dumps({'type': 'search_result', 'username': user['username'] if user else message['username'],
		                                         'found': user is not None, 'online': online is not None,
		                                         'busy': bool(online and online.room), 'rating': user['rating'] if user else None,
		                                         'wins': user['wins'] if user else 0, 'losses': user['losses'] if user else 0}))

	async def on_challenge(self, player, message):
		target_key = str(message['to']).strip().casefold()
		format_name, rule = message['format'], message['rule']
		if format_name not in engine.FORMATS or rule not in engine.TEAM_RULES:
			return await self.error(player.connection, 'bad_challenge')
		if target_key == player.key:
			return await self.error(player.connection, 'challenge_self')
		target = self.players.get(target_key)
		if target is None:
			return await self.error(player.connection, 'player_offline')
		if target.room or player.room:
			return await self.error(player.connection, 'player_busy')
		team = None
		if rule != 'random':
			team, problem = engine.build_team(rule, message.get('team'), engine.FORMATS[format_name][0])
			if problem:
				return await self.error(player.connection, problem)
		challenge_id = uuid.uuid4().hex[:10]
		self.challenges[challenge_id] = {'from': player.key, 'to': target_key, 'format': format_name, 'rule': rule,
		                                 'team': message.get('team'), 'time': time.time()}
		await player.connection.send(json.dumps({'type': 'challenge_sent', 'id': challenge_id, 'to': target.name, 'seconds': CHALLENGE_SECONDS}))
		user = self.db.get_user(player.key)
		await self.send(target_key, {'type': 'challenge_in', 'id': challenge_id, 'from': player.name, 'rating': user['rating'],
		                             'format': format_name, 'rule': rule, 'seconds': CHALLENGE_SECONDS})

	async def on_cancel(self, player, message):
		challenge = self.challenges.get(message['id'])
		if challenge and challenge['from'] == player.key:
			del self.challenges[message['id']]
			await self.send(challenge['to'], {'type': 'challenge_cancelled', 'id': message['id']})

	async def on_answer(self, player, message):
		challenge = self.challenges.get(message['id'])
		if challenge is None or challenge['to'] != player.key:
			return await self.error(player.connection, 'challenge_gone')
		if not message.get('accept'):
			del self.challenges[message['id']]
			return await self.send(challenge['from'], {'type': 'challenge_declined', 'id': message['id'], 'by': player.name})
		challenger = self.players.get(challenge['from'])
		if challenger is None or challenger.room or player.room:
			del self.challenges[message['id']]
			return await self.error(player.connection, 'challenge_gone')
		if challenge['rule'] != 'random':
			_, problem = engine.build_team(challenge['rule'], message.get('team'), engine.FORMATS[challenge['format']][0])
			if problem:
				return await self.error(player.connection, problem)
		del self.challenges[message['id']]
		room = Room(self, {'a': challenger.key, 'b': player.key}, {'a': challenger.name, 'b': player.name},
		            challenge['format'], challenge['rule'], {'a': challenge['team'], 'b': message.get('team')})
		await self.start_battle(room)

	# ---------- battles ----------
	async def start_battle(self, room):
		size, field = engine.FORMATS[room.format]
		if room.rule == 'random':
			teams = {side: engine.random_team(size) for side in engine.SIDES}
		else:
			teams = {side: engine.build_team(room.rule, room.teams_sent[side], size)[0] for side in engine.SIDES}
		room.match = engine.Match(teams['a'], teams['b'], field)
		room.match.take_events()   # the first turn is in the state sent with battle_start
		room.descriptions = {side: [engine.describe(m) for m in teams[side]] for side in engine.SIDES}
		room.ended, room.result, room.rematch = False, None, set()
		self.rooms[room.id] = room
		for side in engine.SIDES:
			player = self.players.get(room.keys[side])
			if player:
				player.room = room
		room.deadline = time.time() + TURN_SECONDS
		for side in engine.SIDES:
			await self.send_start(room, side)

	async def send_start(self, room, side, resume = False):
		users = {s: self.db.get_user(room.keys[s]) for s in engine.SIDES}
		await self.send(room.keys[side], {'type': 'battle_start', 'battle': room.id, 'side': side, 'resume': resume,
		                                  'format': room.format, 'rule': room.rule, 'field': engine.FORMATS[room.format][1],
		                                  'names': room.names, 'ratings': {s: users[s]['rating'] for s in engine.SIDES},
		                                  'teams': room.descriptions, 'state': room.match.state(), 'seconds': TURN_SECONDS,
		                                  'result': room.result})

	async def broadcast(self, room, events):
		if not events:
			return
		if room.match.winner is not None and not room.ended:
			await self.finish(room, events)
			return
		room.deadline = time.time() + TURN_SECONDS
		for side in engine.SIDES:
			await self.send(room.keys[side], {'type': 'events', 'battle': room.id, 'events': events})

	async def on_action(self, player, message):
		room = player.room
		if room is None or room.id != message.get('battle') or room.ended:
			return await self.error(player.connection, 'no_battle')
		problem = room.match.act(room.side_of(player.key), message.get('action'))
		if problem:
			# the game is told, so it can open the menu again (this only happens if the game and server disagree)
			return await player.connection.send(json.dumps({'type': 'action_rejected', 'reason': problem, 'state': room.match.state()}))
		await self.broadcast(room, room.match.take_events())

	async def on_forfeit(self, player, message):
		room = player.room
		if room is not None and not room.ended:
			room.match.forfeit(room.side_of(player.key))
			await self.broadcast(room, room.match.take_events())

	# The battle is over: new ratings, the result saved, and both players told.
	async def finish(self, room, events, reason = None):
		room.ended = True
		match = room.match
		winner = match.winner
		loser = engine.other(winner)
		users = {side: self.db.get_user(room.keys[side]) for side in engine.SIDES}
		new_winner, new_loser = engine.elo(users[winner]['rating'], users[loser]['rating'])
		change = new_winner - users[winner]['rating']
		ratings = {winner: new_winner, loser: new_loser}
		end = next((e for e in events if e['kind'] == 'end'), None)
		reason = reason or (end['reason'] if end else 'knockout')
		self.db.save_result(room.id, room.keys['a'], room.keys['b'], room.keys[winner], room.format, room.rule, reason,
		                    match.turns, change, ratings['a'], ratings['b'], match.log[-300:])
		room.result = {'winner': winner, 'reason': reason, 'change': change,
		               'ratings': {side: [users[side]['rating'], ratings[side]] for side in engine.SIDES}}
		for side in engine.SIDES:
			await self.send(room.keys[side], {'type': 'events', 'battle': room.id, 'events': events})
			await self.send(room.keys[side], {'type': 'battle_end', 'battle': room.id, **room.result})

	async def on_rematch(self, player, message):
		room = player.room
		if room is None or not room.ended:
			return
		side = room.side_of(player.key)
		if room.rule != 'random':
			_, problem = engine.build_team(room.rule, message.get('team'), engine.FORMATS[room.format][0])
			if problem:
				return await self.error(player.connection, problem)
			room.teams_sent[side] = message.get('team')
		room.rematch.add(side)
		if room.rematch == set(engine.SIDES):
			del self.rooms[room.id]
			new = Room(self, room.keys, room.names, room.format, room.rule, room.teams_sent)
			await self.start_battle(new)
		else:
			await self.send(room.keys[engine.other(side)], {'type': 'rematch_asked', 'by': player.name})

	async def on_leave(self, player, message):
		room = player.room
		if room is None:
			return
		side = room.side_of(player.key)
		if not room.ended:
			room.match.forfeit(side)
			await self.broadcast(room, room.match.take_events())
		await self.leave_room(room, side)

	async def leave_room(self, room, side):
		for s in engine.SIDES:
			player = self.players.get(room.keys[s])
			if player is not None and player.room is room and s == side:
				player.room = None
		await self.send(room.keys[engine.other(side)], {'type': 'opponent_gone'})
		other_player = self.players.get(room.keys[engine.other(side)])
		if other_player is None or other_player.room is not room:
			self.rooms.pop(room.id, None)

	# ---------- the rest ----------
	async def on_leaderboard(self, player, message):
		await player.connection.send(json.dumps({'type': 'leaderboard', 'rows': self.db.leaderboard()}))

	async def on_history(self, player, message):
		await player.connection.send(json.dumps({'type': 'history', 'rows': self.db.history(player.key)}))

	async def on_battle_log(self, player, message):
		await player.connection.send(json.dumps({'type': 'battle_log', 'id': message['id'], 'log': self.db.battle_log(str(message['id']), player.key)}))

	async def on_me(self, player, message):
		user = self.db.get_user(player.key)
		await player.connection.send(json.dumps({'type': 'me', 'rating': user['rating'], 'wins': user['wins'], 'losses': user['losses']}))

	async def on_ping(self, player, message):
		await player.connection.send(json.dumps({'type': 'pong'}))

	# Runs every half second: turn time limits, old challenges and players who did not come back.
	async def tick(self):
		while True:
			await asyncio.sleep(0.5)
			now = time.time()
			for challenge_id, challenge in list(self.challenges.items()):
				if now - challenge['time'] > CHALLENGE_SECONDS:
					del self.challenges[challenge_id]
					await self.send(challenge['from'], {'type': 'challenge_expired', 'id': challenge_id})
					await self.send(challenge['to'], {'type': 'challenge_cancelled', 'id': challenge_id})
			for room in list(self.rooms.values()):
				if room.ended:
					if all(self.players.get(k) is None or self.players[k].room is not room for k in room.keys.values()):
						self.rooms.pop(room.id, None)
					continue
				for side, gone in list(room.gone.items()):
					if now - gone > RECONNECT_SECONDS:
						room.match.forfeit(side, 'disconnect')
						await self.broadcast(room, room.match.take_events())
						break
				if not room.ended and room.match.waiting and room.deadline and now > room.deadline:
					room.match.timeout(room.match.waiting[0])
					await self.broadcast(room, room.match.take_events())


# Render (and a web browser) checks the server is alive with a normal web request - answer it with "OK".
def health_check(connection, request):
	if request.headers.get('Upgrade', '').lower() != 'websocket':
		return connection.respond(HTTPStatus.OK, 'Disrupt server is running\n')
	return None


async def main(port = None, database = None, ready = None):
	database = database or Database(os.environ.get('DATABASE_URL', 'disrupt_online.db'))
	server = Server(database)
	port = int(port or os.environ.get('PORT', 8765))
	ticker = asyncio.create_task(server.tick())
	async with serve(server.handle, '0.0.0.0', port, process_request = health_check, max_size = MAX_MESSAGE, ping_interval = 20, ping_timeout = 20) as running:
		log.info('Disrupt server listening on port %s', port)
		if ready is not None:
			ready(server, running)
		try:
			await asyncio.get_running_loop().create_future()   # runs until the program is stopped
		finally:
			ticker.cancel()


if __name__ == '__main__':
	logging.basicConfig(level = logging.INFO, format = '%(asctime)s %(message)s')
	logging.getLogger('websockets').setLevel(logging.WARNING)
	asyncio.run(main())
