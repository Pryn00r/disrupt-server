# online_engine.py
# Iteration 37: the rules of an online battle, run only on the server.
# The server is the one place that decides what happens (who moves next, whether an attack hits, how much
# damage it does). The two players' games only send what they chose ("Fire on the monster in the middle")
# and draw what the server tells them happened. This means:
#   - both players always see exactly the same battle (there is only one copy of it), and
#   - a player who edits their copy of the game cannot cheat - an impossible move is simply rejected.
# The rules are the same as battle.py and battle_rules.py: turn bars filled by speed, energy, the type chart,
# accuracy, critical hits, statuses, stat changes, charge-up moves and priority moves. Nothing here uses
# pygame's drawing, so it can be tested without a window.

import random as random_module

import battle_rules as rules
from game_data import ATTACK_DATA, MONSTER_DATA
from monster import Monster
from save_system import deserialise_monster

SIDES = ('a', 'b')
CRIT_CHANCE = 1 / 16

# format -> (monsters in each team, monsters on the field at once)
FORMATS = {'1v1': (1, 1), '2v2': (2, 2), '3v3': (3, 3), '6v6': (6, 3)}
TEAM_RULES = ('random', 'story', 'built')
ONLINE_LEVEL = 50    # random and built teams are all level 50, so it is a fair fight

# the fully evolved monsters (no 'evolve' entry) - these are the ones used in random and built teams
FINAL_FORMS = [name for name, data in MONSTER_DATA.items() if not data.get('evolve')]


def other(side):
	return 'b' if side == 'a' else 'a'

# A fresh level 50 monster for a random or built team, with full health and energy.
def team_monster(name, moves = None):
	monster = Monster(name, ONLINE_LEVEL)
	if moves:
		known = monster.known_moves()
		chosen = [move for move in dict.fromkeys(moves) if move in known][:4]
		monster.moves = chosen or None
	return monster

def random_team(size, rng = random_module):
	return [team_monster(name) for name in rng.sample(FINAL_FORMS, min(size, len(FINAL_FORMS)))]

# Checks a team a player sent and turns it into Monster objects. Returns (team, None) or (None, error code).
# Every value is checked, because the data came over the internet and could have been edited.
#   story: saved monsters (the same format as a save file) - checked by deserialise_monster
#   built: [{'name': ..., 'moves': [...]}, ...] - only fully evolved monsters, all level 50
def build_team(rule, data, size):
	if not isinstance(data, list) or not data:
		return None, 'team_empty'
	if len(data) > 6:
		return None, 'team_too_big'
	team = []
	try:
		for entry in data:
			if not isinstance(entry, dict):
				return None, 'team_invalid'
			if rule == 'story':
				monster = deserialise_monster(entry)
			else:
				if entry.get('name') not in FINAL_FORMS:
					return None, 'team_invalid'
				moves = entry.get('moves')
				if moves is not None and (not isinstance(moves, list) or any(not isinstance(m, str) or m not in ATTACK_DATA for m in moves)):
					return None, 'team_invalid'
				monster = team_monster(entry['name'], moves)
			team.append(monster)
	except (KeyError, TypeError, ValueError):
		return None, 'team_invalid'
	return team[:size], None

# The data the players' games need to rebuild a monster (sent once, at the start of the battle).
def describe(monster):
	return {'name': monster.name, 'level': monster.level, 'xp': 0, 'health': monster.health, 'energy': monster.energy,
	        'nickname': monster.nickname, 'held_item': monster.held_item, 'shiny': bool(monster.shiny), 'happiness': getattr(monster, 'happiness', 50),
	        'tutored': list(getattr(monster, 'tutored', [])), 'moves': monster.equipped_moves()[:4]}

# Elo rating (the system used in chess). Returns the two new ratings. A win against a higher-rated player
# gains more points than a win against a lower-rated one. K = 32 is the largest change in one battle.
def elo(winner_rating, loser_rating, k = 32):
	expected = 1 / (1 + 10 ** ((loser_rating - winner_rating) / 400))
	change = round(k * (1 - expected))
	return winner_rating + change, loser_rating - change


class Match:
	# team_a / team_b: lists of Monster. field: how many monsters each side has out at once.
	def __init__(self, team_a, team_b, field, seed = None):
		self.rng = random_module.Random(seed)
		self.teams = {'a': list(team_a), 'b': list(team_b)}
		self.field = {side: [i if i < len(self.teams[side]) else None for i in range(field)] for side in SIDES}
		for team in self.teams.values():
			for monster in team:
				monster.health, monster.energy = monster.get_stat('max_health'), monster.get_stat('max_energy')
				monster.initiative, monster.paused, monster.turn_speed = 0, False, 1
				monster.status, monster.status_turns, monster.stages, monster.charging, monster.defending = None, 0, {}, None, False
		self.waiting = None      # (side, position) of the monster whose player must choose an action
		self.winner = None
		self.turns = 0
		self.events = []         # everything that happened since the last call to take_events
		self.log = []            # every message of the battle (kept for the battle history)
		self.advance()

	# ---------- helpers ----------
	def monster_at(self, side, pos):
		if not 0 <= pos < len(self.field[side]):
			return None
		index = self.field[side][pos]
		return None if index is None else self.teams[side][index]

	def active(self):
		return [(side, pos) for side in SIDES for pos, index in enumerate(self.field[side]) if index is not None and self.teams[side][index].health > 0]

	def bench(self, side):
		return [i for i, monster in enumerate(self.teams[side]) if monster.health > 0 and i not in self.field[side]]

	def say(self, key, **values):
		self.log.append([key, values])
		return [key, values]

	def emit(self, kind, **data):
		data['kind'] = kind
		data['state'] = self.state()
		self.events.append(data)

	def take_events(self):
		events, self.events = self.events, []
		return events

	# Everything the players' games need to draw the battle right now.
	def state(self):
		return {
			'field': {side: list(self.field[side]) for side in SIDES},
			'teams': {side: [{'health': round(m.health, 3), 'energy': round(m.energy, 3), 'status': m.status, 'stages': dict(m.stages),
			                  'initiative': round(m.initiative, 2), 'charging': m.charging[1] if m.charging else None, 'defending': m.defending}
			                 for m in self.teams[side]] for side in SIDES},
			'waiting': list(self.waiting) if self.waiting else None,
			'winner': self.winner}

	# ---------- turn order ----------
	# Finds the monster that would fill its turn bar first, moves every bar on by that much, and starts that
	# monster's turn. The same as battle.py's real-time bars, worked out in one step instead of frame by frame.
	# Ties go to side 'a' then the higher position, so the order never depends on luck or timing.
	def advance(self):
		while self.winner is None:
			if self.check_winner():
				return
			candidates = []
			for side, pos in self.active():
				monster = self.monster_at(side, pos)
				speed = max(monster.get_stat('speed'), 0.001)
				candidates.append((max(0, 100 - monster.initiative) / speed, SIDES.index(side), pos, side))
			wait, _, pos, side = min(candidates)
			for other_side, other_pos in self.active():
				monster = self.monster_at(other_side, other_pos)
				monster.initiative += monster.get_stat('speed') * wait
			if self.start_turn(side, pos):
				return

	# Returns True if the battle now waits for a player, False if the turn was used up automatically.
	def start_turn(self, side, pos):
		monster = self.monster_at(side, pos)
		monster.initiative = 0
		monster.defending = False
		monster.regain_energy()
		self.turns += 1
		roll = self.rng.random()
		can_act, message, damage = rules.start_of_turn(monster, roll)
		monster.stat_limiter()
		if message:
			self.emit('status', who = [side, pos], message = self.say(message, monster = monster.display_name), damage = round(damage, 2))
		if monster.health <= 0:
			self.after_action()
			return False
		if not can_act:
			return False
		if monster.charging:   # a charged move is released now, with no choice to make
			target, attack = monster.charging
			monster.charging = None
			target_side = side if ATTACK_DATA[attack]['target'] == 'player' else other(side)
			if target is None or self.monster_at(*target) is None or self.monster_at(*target).health <= 0:
				options = [p for s, p in self.active() if s == target_side]
				target = (target_side, self.rng.choice(options)) if options else None
			if target is not None:
				self.hit(side, pos, target, attack)
			self.after_action()
			return False
		self.waiting = (side, pos)
		self.emit('turn', who = [side, pos])
		return True

	# ---------- the players' choices ----------
	# Called when a player sends an action. Returns None if it was carried out, or the reason it was rejected.
	# action: {'type': 'move', 'move': name, 'target': [side, pos]} / {'type': 'defend'} / {'type': 'switch', 'index': i}
	def act(self, side, action):
		if self.winner is not None:
			return 'battle_over'
		if self.waiting is None or self.waiting[0] != side:
			return 'not_your_turn'
		if not isinstance(action, dict):
			return 'bad_action'
		pos = self.waiting[1]
		monster = self.monster_at(side, pos)
		kind = action.get('type')
		if kind == 'move':
			attack = action.get('move')
			target = action.get('target')
			if attack not in monster.get_abilities(all = False):   # must be one of its 4 moves and affordable
				return 'bad_move'
			if not (isinstance(target, list) and len(target) == 2 and target[0] in SIDES and isinstance(target[1], int)):
				return 'bad_target'
			wanted_side = side if ATTACK_DATA[attack]['target'] == 'player' else other(side)
			target_monster = self.monster_at(target[0], target[1])
			if target[0] != wanted_side or target_monster is None or target_monster.health <= 0:
				return 'bad_target'
			self.waiting = None
			self.use_move(side, pos, (target[0], target[1]), attack)
		elif kind == 'defend':
			self.waiting = None
			monster.defend()
			self.emit('defend', who = [side, pos], message = self.say('online_defends', monster = monster.display_name))
		elif kind == 'switch':
			index = action.get('index')
			if not isinstance(index, int) or isinstance(index, bool) or index not in self.bench(side):
				return 'bad_switch'
			self.waiting = None
			self.field[side][pos] = index
			new = self.teams[side][index]
			new.initiative = 0
			self.emit('switch', who = [side, pos], index = index, message = self.say('online_switched', monster = new.display_name))
		else:
			return 'bad_action'
		self.after_action()
		self.advance()
		return None

	# A player whose time ran out defends automatically.
	def timeout(self, side):
		if self.waiting and self.waiting[0] == side:
			self.act(side, {'type': 'defend'})

	def forfeit(self, side, reason = 'forfeit'):
		if self.winner is None:
			self.winner = other(side)
			self.waiting = None
			self.emit('end', winner = self.winner, reason = reason)

	# ---------- moves ----------
	def use_move(self, side, pos, target, attack):
		monster = self.monster_at(side, pos)
		monster.reduce_energy(attack)
		if rules.is_charge(attack) or rules.priority(attack) < 0:
			monster.charging = (target, attack)
			monster.initiative = 0 if rules.is_charge(attack) else rules.LAST_WAIT
			key = 'battle_charging' if rules.is_charge(attack) else 'battle_waiting'
			self.emit('charge', who = [side, pos], move = attack, message = self.say(key, monster = monster.display_name, attack = attack))
			return
		self.hit(side, pos, target, attack)
		if rules.priority(attack) > 0:
			monster.initiative = rules.PRIORITY_HEAD_START

	# What happens when an attack lands - the same steps as Battle.apply_attack.
	def hit(self, side, pos, target, attack):
		attacker = self.monster_at(side, pos)
		defender = self.monster_at(*target)
		data = ATTACK_DATA[attack]
		result = {'who': [side, pos], 'target': list(target), 'move': attack, 'messages': []}
		name = attacker.display_name
		critical = self.rng.random() < CRIT_CHANCE * (2 if attacker.is_happy() else 1)
		if not rules.hits(attack, self.rng.random()):
			result['missed'] = True
			result['messages'].append(self.say('battle_missed', monster = name, attack = attack))
		elif data.get('kind') == 'heal':
			healed = min(defender.get_stat('max_health') - defender.health, defender.get_stat('max_health') * data['heal'])
			defender.health += healed
			result['healed'] = round(healed, 2)
			result['messages'].append(self.say('battle_healed' if healed > 0 else 'battle_no_effect', monster = defender.display_name))
		elif rules.is_status_move(attack):
			result['messages'].append(self.side_effects(defender, attack, status_move = True))
		else:
			amount = attacker.get_base_damage(attack) * (1.5 if critical else 1)
			multiplier, effect = rules.effectiveness(data['element'], *rules.types_of(defender))
			defence = 1 - defender.get_stat('defense') / 2000 - (0.2 if defender.defending else 0)
			damage = amount * multiplier * max(0, min(1, defence)) * rules.DAMAGE_SCALE
			defender.health -= damage
			result.update(damage = round(damage, 2), effect = effect, critical = critical)
			result['messages'].append(self.say('battle_used', monster = name, attack = attack, effect = effect))
			if critical:
				result['messages'].append(self.say('battle_critical'))
			if defender.health > 0:
				if defender.status == 'freeze' and data['element'] == 'fire':
					defender.status = None
				extra = self.side_effects(defender, attack, status_move = False)
				if extra:
					result['messages'].append(extra)
			self_status = data.get('self_status')
			if self_status and attacker.health > 0 and not attacker.status and self.rng.random() < self_status[1]:
				rules.give_status(attacker, self_status[0])
				result['messages'].append(self.say(f'status_given_{self_status[0]}', monster = name))
		defender.stat_limiter()
		self.emit('attack', **result)

	def side_effects(self, defender, attack, status_move):
		data = ATTACK_DATA[attack]
		status = rules.try_status(defender, attack, self.rng.random())
		if status:
			return self.say(f'status_given_{status}', monster = defender.display_name)
		if 'stat' in data and (status_move or self.rng.random() < data.get('stat_chance', 1)):
			stat, change = data['stat']
			done = rules.change_stage(defender, stat, change)
			key = 'stat_fell' if done < 0 else 'stat_rose' if done > 0 else 'stat_unchanged'
			return self.say(key, monster = defender.display_name, stat = stat)
		return self.say('battle_no_effect', monster = defender.display_name) if status_move else None

	# Knocked out monsters are replaced by the next healthy one in the team, in the same place.
	def after_action(self):
		for side in SIDES:
			for pos, index in enumerate(self.field[side]):
				if index is None or self.teams[side][index].health > 0:
					continue
				fainted = self.teams[side][index]
				fainted.charging = None
				bench = self.bench(side)
				self.field[side][pos] = bench[0] if bench else None
				self.emit('faint', who = [side, pos], index = index, replacement = self.field[side][pos],
				          message = self.say('online_fainted', monster = fainted.display_name))
		self.check_winner()

	def check_winner(self):
		if self.winner is not None:
			return True
		for side in SIDES:
			if not any(m.health > 0 for m in self.teams[side]):
				self.winner = other(side)
				self.waiting = None
				self.emit('end', winner = self.winner, reason = 'knockout')
				return True
		return False
