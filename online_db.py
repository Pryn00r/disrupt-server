# online_db.py
# Iteration 37: the online server's database - accounts, ratings and the battle history.
# On my computer it uses SQLite (one file, nothing to install). On the real server it uses PostgreSQL,
# because the free server's own disk is wiped every time it restarts; the database lives at Neon instead
# and its address is given to the server in the DATABASE_URL setting. The SQL is the same for both.

import json
import sqlite3
import threading
import time

TABLES = (
	'''CREATE TABLE IF NOT EXISTS users (
		username_key TEXT PRIMARY KEY,   -- the username in lower case, so "Speedy" and "speedy" are the same account
		username TEXT NOT NULL,
		salt TEXT NOT NULL,
		password_hash TEXT NOT NULL,
		token_hash TEXT,
		rating INTEGER NOT NULL DEFAULT 1000,
		wins INTEGER NOT NULL DEFAULT 0,
		losses INTEGER NOT NULL DEFAULT 0,
		created REAL NOT NULL)''',
	'''CREATE TABLE IF NOT EXISTS battles (
		id TEXT PRIMARY KEY,
		player_a TEXT NOT NULL REFERENCES users(username_key),
		player_b TEXT NOT NULL REFERENCES users(username_key),
		winner TEXT NOT NULL,
		format TEXT NOT NULL,
		team_rule TEXT NOT NULL,
		reason TEXT NOT NULL,
		turns INTEGER NOT NULL,
		rating_change INTEGER NOT NULL,
		created REAL NOT NULL,
		log TEXT NOT NULL)''',
	'CREATE INDEX IF NOT EXISTS battles_a ON battles(player_a)',
	'CREATE INDEX IF NOT EXISTS battles_b ON battles(player_b)',
)


class Database:
	# address: a file name for SQLite, or a postgres:// address for PostgreSQL
	def __init__(self, address):
		self.address = address
		self.postgres = address.startswith(('postgres://', 'postgresql://'))
		self.lock = threading.Lock()
		self.connection = None
		self.connect()
		for sql in TABLES:
			self.run(sql)

	def connect(self):
		if self.postgres:
			import psycopg
			self.connection = psycopg.connect(self.address, autocommit = True)
		else:
			self.connection = sqlite3.connect(self.address, check_same_thread = False, isolation_level = None)

	# Runs one SQL statement with ? placeholders (changed to %s for PostgreSQL) and returns the rows.
	# Parameters are always passed separately from the SQL, never pasted into it, so a username like
	# "x'; DROP TABLE users; --" is stored as text and cannot change the command (SQL injection).
	def run(self, sql, parameters = ()):
		if self.postgres:
			sql = sql.replace('?', '%s')
		with self.lock:
			for attempt in (1, 2):
				try:
					cursor = self.connection.cursor()
					cursor.execute(sql, parameters)
					rows = cursor.fetchall() if cursor.description else []
					cursor.close()
					return rows
				except Exception as error:
					# Neon closes a connection that has been idle for a while - connect again once
					if self.postgres and attempt == 1 and type(error).__name__ in ('OperationalError', 'InterfaceError'):
						self.connect()
						continue
					raise

	# ---------- accounts ----------
	def get_user(self, key):
		rows = self.run('SELECT username, salt, password_hash, token_hash, rating, wins, losses FROM users WHERE username_key = ?', (key,))
		if not rows:
			return None
		username, salt, password_hash, token_hash, rating, wins, losses = rows[0]
		return {'key': key, 'username': username, 'salt': salt, 'password_hash': password_hash, 'token_hash': token_hash,
		        'rating': rating, 'wins': wins, 'losses': losses}

	def create_user(self, key, username, salt, password_hash):
		self.run('INSERT INTO users (username_key, username, salt, password_hash, created) VALUES (?, ?, ?, ?, ?)',
		         (key, username, salt, password_hash, time.time()))

	def set_token(self, key, token_hash):
		self.run('UPDATE users SET token_hash = ? WHERE username_key = ?', (token_hash, key))

	def set_password(self, key, salt, password_hash):
		self.run('UPDATE users SET salt = ?, password_hash = ?, token_hash = NULL WHERE username_key = ?', (salt, password_hash, key))

	# ---------- results ----------
	def save_result(self, battle_id, key_a, key_b, winner, format_name, rule, reason, turns, change, rating_a, rating_b, log):
		self.run('INSERT INTO battles (id, player_a, player_b, winner, format, team_rule, reason, turns, rating_change, created, log) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
		         (battle_id, key_a, key_b, winner, format_name, rule, reason, turns, change, time.time(), json.dumps(log)))
		won_a = winner == key_a
		self.run('UPDATE users SET rating = ?, wins = wins + ?, losses = losses + ? WHERE username_key = ?', (rating_a, int(won_a), int(not won_a), key_a))
		self.run('UPDATE users SET rating = ?, wins = wins + ?, losses = losses + ? WHERE username_key = ?', (rating_b, int(not won_a), int(won_a), key_b))

	# the top players: highest rating first, then most wins
	def leaderboard(self, limit = 20):
		return [list(row) for row in self.run('SELECT username, rating, wins, losses FROM users WHERE wins + losses > 0 ORDER BY rating DESC, wins DESC LIMIT ?', (limit,))]

	# a player's most recent battles, newest first (a JOIN gets the opponent's display name)
	def history(self, key, limit = 15):
		rows = self.run('''SELECT b.id, b.player_a, b.player_b, b.winner, b.format, b.team_rule, b.reason, b.turns, b.rating_change, b.created, ua.username, ub.username
		                   FROM battles b JOIN users ua ON ua.username_key = b.player_a JOIN users ub ON ub.username_key = b.player_b
		                   WHERE b.player_a = ? OR b.player_b = ? ORDER BY b.created DESC LIMIT ?''', (key, key, limit))
		history = []
		for battle_id, a, b, winner, format_name, rule, reason, turns, change, created, name_a, name_b in rows:
			history.append({'id': battle_id, 'opponent': name_b if a == key else name_a, 'won': winner == key, 'format': format_name, 'rule': rule,
			                'reason': reason, 'turns': turns, 'change': change if winner == key else -change, 'date': time.strftime('%Y-%m-%d', time.gmtime(created))})
		return history

	def battle_log(self, battle_id, key):
		rows = self.run('SELECT log FROM battles WHERE id = ? AND (player_a = ? OR player_b = ?)', (battle_id, key, key))
		return json.loads(rows[0][0]) if rows else None
