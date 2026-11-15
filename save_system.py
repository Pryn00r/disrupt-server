# save_system.py
# Everything to do with files: protected reading/writing with checksums and backups, username
# validation, player profiles, the three save slots per player, and converting monsters to and from JSON.

import hashlib
import hmac
import json
import os
import shutil
import time
import uuid
from datetime import datetime
from os.path import abspath, dirname, exists, join

from monster import Monster
from game_data import HELD_ITEM_DATA, ATTACK_DATA, current_name, current_move
from settings import (RESERVED_USERNAMES, SAVE_SLOT_COUNT, USERNAME_MAX_LENGTH, USERNAME_MIN_LENGTH,
	PASSWORD_MIN_LENGTH, PASSWORD_MAX_LENGTH, PASSWORD_SYMBOLS, SECURITY_QUESTIONS, MAX_SIGN_IN_ATTEMPTS, LOCKOUT_SECONDS, MOVE_SLOTS)

# folder that holds every save file, and the save format version (so old saves could be upgraded later)
SAVE_ROOT = join(dirname(abspath(__file__)), 'saves')
SAVE_VERSION = 1


# protected files
# Returns a SHA-256 hash of the data. If even one character of a save is changed, the hash changes,
# so a damaged file, or one edited by hand, can be detected.
# Limitation: there is no secret key, so someone who reads this code could edit a save AND work out
# the new checksum. It protects against accidents and casual editing, not against a determined cheater.
def get_checksum(data):
	text = json.dumps(data, sort_keys = True, separators = (',', ':'))
	return hashlib.sha256(text.encode('utf-8')).hexdigest()

# Reads a protected file and returns its data. Raises ValueError if the checksum does not match.
def read_verified(path):
	with open(path, encoding = 'utf-8') as file:
		payload = json.load(file)
	if payload['checksum'] != get_checksum(payload['data']):
		raise ValueError(f'checksum mismatch in {path}')
	return payload['data']

# Returns True if the file exists, is valid JSON and passes its checksum.
def is_valid_file(path):
	try:
		read_verified(path)
		return True
	except (OSError, ValueError, KeyError, TypeError):
		return False

# Safely writes data to a file with a checksum. The old file becomes the .bak backup (only if it was
# valid), and the new data is written to a .tmp file first then swapped in, so a crash mid-write cannot
# leave a half-written save.
def write_protected(path, data):
	# the backup is only replaced by a file that has passed its checksum
	os.makedirs(dirname(path), exist_ok = True)
	if is_valid_file(path):
		shutil.copy2(path, f'{path}.bak')

	# writing to a temporary file first means a crash cannot damage the real file
	payload = {'version': SAVE_VERSION, 'checksum': get_checksum(data), 'data': data}
	temporary_path = f'{path}.tmp'
	with open(temporary_path, 'w', encoding = 'utf-8') as file:
		json.dump(payload, file, indent = 2)
		file.flush()
		os.fsync(file.fileno())
	os.replace(temporary_path, path)

# Returns the data from the file, or from its backup if the main file is damaged, or None if both are bad.
def read_protected(path):
	for candidate in (path, f'{path}.bak'):
		if is_valid_file(candidate):
			return read_verified(candidate)
	return None


# usernames
# Validation for a new username. Returns None if valid, or the key of the error message to show:
# length check (3-12), format check (letters, numbers, underscores only), lookup check against reserved
# names, and a duplicate check that ignores capital letters.
def validate_username(username, existing_usernames):
	name = username.strip()
	if len(name) < USERNAME_MIN_LENGTH:
		return 'username_too_short'
	if len(name) > USERNAME_MAX_LENGTH:
		return 'username_too_long'
	if not all(character.isascii() and (character.isalnum() or character == '_') for character in name):
		return 'username_invalid'
	if name.casefold() in RESERVED_USERNAMES:
		return 'username_reserved'
	if name.casefold() in {existing.casefold() for existing in existing_usernames}:
		return 'username_taken'
	return None


# passwords (Iteration 14)
# Validation for a new password. Returns None if valid, or the key of the first rule it breaks:
# length check (8-24), at least one uppercase letter, lowercase letter, number and symbol, no character
# repeated 3 or more times in a row (e.g. 555) and it must not contain the username.
def validate_password(password, username = ''):
	if len(password) < PASSWORD_MIN_LENGTH:
		return 'password_too_short'
	if len(password) > PASSWORD_MAX_LENGTH:
		return 'password_too_long'
	for error, rule in password_rules(password, username):
		if not rule:
			return error
	return None

# Returns [(error key, passed?), ...] for every password rule. Used by validate_password and by the
# sign up screen, which ticks each rule off live while the player types.
def password_rules(password, username = ''):
	repeated = any(password[i] == password[i + 1] == password[i + 2] for i in range(len(password) - 2))
	return [
		('password_too_short', PASSWORD_MIN_LENGTH <= len(password) <= PASSWORD_MAX_LENGTH),
		('password_no_upper', any(character.isupper() for character in password)),
		('password_no_lower', any(character.islower() for character in password)),
		('password_no_number', any(character.isdigit() for character in password)),
		('password_no_symbol', any(character in PASSWORD_SYMBOLS for character in password)),
		('password_repeated', not repeated),
		('password_has_username', not username or username.casefold() not in password.casefold())]

# Returns a salted hash of a password or security answer. The real text is never saved - only this hash.
# PBKDF2 runs SHA-256 100,000 times so guessing passwords from a copied file would be very slow.
def hash_secret(text, salt):
	return hashlib.pbkdf2_hmac('sha256', text.encode('utf-8'), salt.encode('utf-8'), 100_000).hex()

# Security answers are compared without capitals or extra spaces, so "Max " and "max" both work.
def normalise_answer(answer):
	return ' '.join(answer.split()).casefold()

# Validation for a security answer: must be 2-30 characters once spaces are removed.
def validate_answer(answer):
	return None if 2 <= len(normalise_answer(answer)) <= 30 else 'answer_invalid'


# Stores the list of players (accounts) in profiles.json.
# Iteration 14: each profile also stores a password hash, a salt, a security question and a hash of its answer.
class ProfileManager:
	def __init__(self, root = SAVE_ROOT):
		self.root = root
		self.path = join(root, 'profiles.json')
		data = read_protected(self.path)
		self.profiles = data['profiles'] if data else []
		self.failed = {}   # username -> (failed attempts, time of the last one), only kept while the game is open

	# Writes every profile to profiles.json.
	def save(self):
		write_protected(self.path, {'profiles': self.profiles})

	# Returns the profile with this username (capitals ignored), or None. Linear search.
	def find(self, username):
		for profile in self.profiles:
			if profile['username'].casefold() == username.strip().casefold():
				return profile
		return None

	# Stores a new password (and optionally a new security question and answer) as salted hashes.
	# The answer has its own salt, so changing the password does not break the security answer.
	def set_password(self, profile, password, question = None, answer = None):
		profile['salt'] = os.urandom(16).hex()   # a new random salt every time
		profile['password_hash'] = hash_secret(password, profile['salt'])
		profile.pop('session_hash', None)        # a new password signs this account out everywhere
		if question is not None:
			profile['question'] = question
			profile['answer_salt'] = os.urandom(16).hex()
			profile['answer_hash'] = hash_secret(normalise_answer(answer), profile['answer_salt'])
		self.save()

	# Returns True if the security answer matches (capitals and extra spaces ignored).
	@staticmethod
	def check_answer(profile, answer):
		if 'answer_hash' not in profile:
			return False
		return hmac.compare_digest(profile['answer_hash'], hash_secret(normalise_answer(answer), profile['answer_salt']))

	# Returns True if the password matches. compare_digest takes the same time whether or not it matches.
	@staticmethod
	def check_password(profile, password):
		if 'password_hash' not in profile:
			return False
		return hmac.compare_digest(profile['password_hash'], hash_secret(password, profile['salt']))

	# Signs a player in. Returns (profile, None) or (None, error key). After MAX_SIGN_IN_ATTEMPTS wrong
	# passwords the account is locked for LOCKOUT_SECONDS. Accounts made before passwords existed
	# return (profile, 'needs_password') so the player is asked to set one.
	def sign_in(self, username, password, now = None):
		now = time.time() if now is None else now
		profile = self.find(username)
		if profile is None:
			return None, 'sign_in_failed'   # same message as a wrong password, so usernames cannot be guessed
		if self.is_locked(profile, now):
			return None, 'account_locked'
		if 'password_hash' not in profile:
			return profile, 'needs_password'
		if not self.check_password(profile, password):
			self.record_failure(profile, now)
			return None, 'sign_in_failed'
		self.failed.pop(profile['id'], None)
		return profile, None

	# ---------- Iteration 37: stay signed in until the player logs out ----------
	# Signing in writes session.json with a random 64-character token. Only a hash of the token is kept in
	# profiles.json, so copying profiles.json alone is not enough to sign in as someone, and because the
	# hash uses the password salt, changing or resetting the password makes an old session.json useless.
	def remember(self, profile):
		token = os.urandom(32).hex()
		profile['session_hash'] = hash_secret(token, profile['salt'])
		self.save()
		write_protected(join(self.root, 'session.json'), {'id': profile['id'], 'token': token})

	# Returns the profile that is still signed in from last time, or None (no session, a damaged or
	# edited file, a deleted account, or a password changed since).
	def restore_session(self):
		path = join(self.root, 'session.json')
		if not exists(path):
			return None
		try:
			data = read_verified(path)
			profile = next((p for p in self.profiles if p['id'] == data['id']), None)
			if profile is None or 'session_hash' not in profile or 'salt' not in profile:
				return None
			if hmac.compare_digest(profile['session_hash'], hash_secret(str(data['token']), profile['salt'])):
				return profile
		except (OSError, ValueError, KeyError, TypeError):
			pass
		return None

	# Logging out: the token is removed from the profile and session.json (and any backup) is deleted.
	def forget(self, profile = None):
		if profile is not None and profile.pop('session_hash', None) is not None:
			self.save()
		for path in (join(self.root, 'session.json'), join(self.root, 'session.json.bak'), join(self.root, 'session.json.tmp')):
			if exists(path):
				os.remove(path)

	# Returns True if the account has had too many wrong passwords/answers in the last LOCKOUT_SECONDS.
	def is_locked(self, profile, now):
		attempts, last = self.failed.get(profile['id'], (0, 0))
		return attempts >= MAX_SIGN_IN_ATTEMPTS and now - last < LOCKOUT_SECONDS

	# Counts one wrong attempt. The count starts again once the lockout time has passed.
	def record_failure(self, profile, now):
		attempts, last = self.failed.get(profile['id'], (0, 0))
		attempts = 0 if now - last >= LOCKOUT_SECONDS else attempts
		self.failed[profile['id']] = (attempts + 1, now)

	# Changes a password after checking the old one. Returns None or an error key.
	def change_password(self, profile, old_password, new_password):
		if not self.check_password(profile, old_password):
			return 'password_wrong'
		if self.check_password(profile, new_password):
			return 'password_same'
		error = validate_password(new_password, profile['username'])
		if error:
			return error
		self.set_password(profile, new_password)
		return None

	# Forgotten password: checks the security answer, then sets the new password. Returns None or an error key.
	def reset_password(self, username, answer, new_password, now = None):
		now = time.time() if now is None else now
		profile = self.find(username)
		if profile is None:
			return 'answer_wrong'
		if self.is_locked(profile, now):
			return 'account_locked'   # stops someone guessing the answer over and over
		if not self.check_answer(profile, answer):
			self.record_failure(profile, now)
			return 'answer_wrong'
		error = validate_password(new_password, profile['username'])
		if error:
			return error
		self.set_password(profile, new_password)
		return None

	# Changes a username (paid for with coins in the game). Returns None or an error key.
	def rename(self, profile, new_username):
		others = [name for name in self.usernames() if name != profile['username']]
		error = validate_username(new_username, others)
		if error:
			return error
		if new_username.strip() == profile['username']:
			return 'username_same'
		profile['username'] = new_username.strip()
		self.save()
		return None

	# Returns a list of every username.
	def usernames(self):
		return [profile['username'] for profile in self.profiles]

	# Validates and saves a new account. Each player gets a random unique id so their folder name never clashes.
	# Returns (profile, None) on success or (None, error key) if anything is rejected.
	def create(self, username, password, question, answer):
		error = (validate_username(username, self.usernames()) or validate_password(password, username.strip())
			or (None if question in SECURITY_QUESTIONS else 'question_invalid') or validate_answer(answer))
		if error:
			return None, error
		profile = {
			'id': uuid.uuid4().hex,
			'username': username.strip(),
			'created': datetime.now().strftime('%Y-%m-%d %H:%M')}
		self.profiles.append(profile)
		self.set_password(profile, password, question, answer)   # also saves profiles.json
		return profile, None

	# Returns the SaveManager for one player's three slots.
	def get_saves(self, profile):
		return SaveManager(profile, self.root)

	# Builds the leaderboard: each player's best slot by score, sorted highest first, then by username.
	def leaderboard(self):
		# each player is ranked by the best score across their own save slots
		entries = []
		for profile in self.profiles:
			saves = [slot['data'] for slot in self.get_saves(profile).all_slots() if slot['status'] == 'ok']
			if saves:
				best = max(saves, key = calculate_score)
				# Iteration 25: the other boards use each player's best save for that board
				progress = [save.get('progress', {}) if isinstance(save.get('progress'), dict) else {} for save in saves]
				finishes = [p.get('story', {}).get('finish_time') for p in progress if isinstance(p.get('story'), dict)]
				finishes = [time for time in finishes if isinstance(time, int)]
				entries.append({
					'id': profile['id'],
					'username': profile['username'],
					'score': calculate_score(best),
					'trainers': len(best['defeated_trainers']),
					'top_level': max(monster['level'] for monster in best['party']),
					'caught': max((len(p.get('caught', [])) for p in progress), default = 0),
					'shiny': max((p.get('counters', {}).get('shiny', 0) for p in progress), default = 0),
					'finish': min(finishes) if finishes else None})
			else:
				# Iteration 14: players with no saves are still listed so everyone can be seen
				entries.append({'id': profile['id'], 'username': profile['username'], 'score': 0, 'trainers': 0, 'top_level': '-', 'caught': 0, 'shiny': 0, 'finish': None})
		return sorted(entries, key = lambda entry: (-entry['score'], entry['username'].casefold()))


# Reads, writes and deletes one player's save slots. Each player has their own folder so their saves are separate.
class SaveManager:
	def __init__(self, profile, root = SAVE_ROOT):
		self.profile = profile
		self.folder = join(root, f"profile_{profile['id']}")

	# Returns the file path of a slot, e.g. saves/profile_<id>/slot_1.json
	def slot_path(self, slot):
		return join(self.folder, f'slot_{slot}.json')

	def write_slot(self, slot, data):
		write_protected(self.slot_path(slot), data)

	def read_slot(self, slot):
		return read_protected(self.slot_path(slot))

	def delete_slot(self, slot):
		for path in (self.slot_path(slot), f'{self.slot_path(slot)}.bak'):
			if exists(path):
				os.remove(path)

	# Returns the slot's status: 'ok' (with its data), 'empty' or 'corrupted' (files exist but fail their checksum).
	def slot_info(self, slot):
		path = self.slot_path(slot)
		data = self.read_slot(slot)
		if data:
			return {'slot': slot, 'status': 'ok', 'data': data}
		has_files = exists(path) or exists(f'{path}.bak')
		return {'slot': slot, 'status': 'corrupted' if has_files else 'empty', 'data': None}

	# Returns slot_info for slots 1 to SAVE_SLOT_COUNT.
	def all_slots(self):
		return [self.slot_info(slot) for slot in range(1, SAVE_SLOT_COUNT + 1)]


# game data conversion
# Converts a Monster object into a dictionary that can be stored as JSON.
def serialise_monster(monster):
	return {
		'name': monster.name,
		'level': monster.level,
		'xp': monster.xp,
		'health': monster.health,
		'energy': monster.energy,
		'nickname': monster.nickname,     # Iteration 13
		'held_item': monster.held_item,   # Iteration 13
		'shiny': monster.shiny,           # Iteration 16
		'declined': getattr(monster, 'declined', 0),   # Iteration 25: the level its evolution was stopped at
		'happiness': getattr(monster, 'happiness', 50),
		'tutored': list(getattr(monster, 'tutored', [])),
		'moves': list(monster.moves) if getattr(monster, 'moves', None) is not None else None}   # Iteration 32

# Rebuilds a Monster from saved data. Monster() validates the name and level, and stat_limiter keeps
# health and energy in range, so an edited save cannot create an invalid monster.
def deserialise_monster(data):
	monster = Monster(current_name(data['name']), int(data['level']))   # Iteration 26: renamed species
	monster.xp = data['xp']
	monster.health = data['health']
	monster.energy = data['energy']
	# Iteration 13: older saves have no nickname or held item, so .get gives None instead of a KeyError.
	# set_nickname validates the text and the held item is only kept if it is a real item (lookup check).
	if not monster.set_nickname(data.get('nickname') or ''):
		raise ValueError('invalid nickname')
	held_item = data.get('held_item')
	if held_item is not None and held_item not in HELD_ITEM_DATA:
		raise ValueError(f'unknown held item {held_item!r}')
	monster.held_item = held_item
	monster.shiny = data.get('shiny', False) is True   # type check: only a real True makes it shiny
	declined = data.get('declined', 0)
	if not isinstance(declined, int) or isinstance(declined, bool) or declined < 0:
		raise ValueError('invalid declined level')
	monster.declined = declined
	happiness = data.get('happiness', 50)
	if not isinstance(happiness, int) or isinstance(happiness, bool) or not 0 <= happiness <= 255:
		raise ValueError('invalid happiness')
	monster.happiness = happiness
	# Iteration 32: the 4 moves chosen for battle (None in older saves = the 4 newest)
	moves = data.get('moves')
	if isinstance(moves, list):   # Iteration 35: removed or renamed moves become their replacement (no repeats)
		moves = list(dict.fromkeys(current_move(move) if isinstance(move, str) else move for move in moves))
	if moves is not None and (not isinstance(moves, list) or not 1 <= len(moves) <= MOVE_SLOTS or any(move not in ATTACK_DATA for move in moves)):
		raise ValueError('invalid moves')
	monster.moves = moves
	tutored = data.get('tutored', [])
	if isinstance(tutored, list):
		tutored = [current_move(move) if isinstance(move, str) else move for move in tutored]
	if not isinstance(tutored, list) or len(tutored) > 2 or any(move not in ATTACK_DATA for move in tutored):
		raise ValueError('invalid tutored moves')
	monster.tutored = list(tutored)
	monster.stat_limiter()
	return monster

# Leaderboard score = 100 per trainer defeated + the total level of the party.
def calculate_score(data):
	return len(data['defeated_trainers']) * 100 + sum(monster['level'] for monster in data['party'])

# Converts seconds into hh:mm for display.
def format_play_time(seconds):
	minutes = int(seconds) // 60
	return f'{minutes // 60:02}:{minutes % 60:02}'
