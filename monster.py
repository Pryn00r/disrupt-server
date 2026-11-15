# monster.py
# Contains the Monster class, which stores the data for a single monster (stats, health,
# energy, experience and evolution). Every monster in the game - the player's party,
# trainers' monsters and wild monsters - is created from this one class.
# Used by: main.py, entities.py (trainer monsters), battle.py, monster_index.py

from game_data import MONSTER_DATA, ATTACK_DATA, HELD_ITEM_DATA
from settings import ENERGY_PER_TURN, DEFEND_ENERGY, MOVE_SLOTS
from battle_rules import stage_multiplier, BURN_ATTACK

# lowest and highest level a monster is allowed to have (used by the level range check)
MIN_LEVEL = 1
MAX_LEVEL = 100

# experience needed per level, e.g. a level 10 monster needs 10 * 150 = 1500 xp to level up
XP_PER_LEVEL = 150

# longest nickname a player can give a monster (Iteration 13)
NICKNAME_MAX_LENGTH = 12

class Monster:
	# Constructor - creates a monster of the given species at the given level.
	# Parameters: name (string, must be a key in MONSTER_DATA), level (integer 1-100)
	# Raises ValueError / TypeError with a clear message if the data is invalid (validation).
	# Called from: Game.__init__, Game.monster_encounter, Game.check_evolution, Character.__init__
	def __init__(self, name, level):
		# --- validation (see section 3.5 of my write-up) ---
		# lookup check: the species must exist in MONSTER_DATA
		if name not in MONSTER_DATA:
			raise ValueError(f'"{name}" is not a monster in MONSTER_DATA')
		# type check: level must be a whole number (bool is excluded because True counts as 1 in Python)
		if not isinstance(level, int) or isinstance(level, bool):
			raise TypeError(f'level must be an integer, got {level!r}')
		# range check: level must be between MIN_LEVEL and MAX_LEVEL
		if not MIN_LEVEL <= level <= MAX_LEVEL:
			raise ValueError(f'level must be between {MIN_LEVEL} and {MAX_LEVEL}, got {level}')

		self.name, self.level = name, level   # species name (string) and current level (integer)
		self.paused = False                     # True while another monster is taking its turn, stops initiative rising
		self.turn_speed = 1                     # set by Battle so slow battles are sped up (Iteration 14)

		# stats
		self.element = MONSTER_DATA[name]['stats']['element']           # 'fire', 'water' or 'plant'
		self.element2 = MONSTER_DATA[name]['stats'].get('element2')      # Iteration 27: a second type, or None
		self.base_stats = MONSTER_DATA[name]['stats']                   # stats at level 1, scaled by get_stat()
		self.health = self.base_stats['max_health'] * self.level        # current health, starts full
		self.energy = self.base_stats['max_energy'] * self.level        # current energy, used to pay for attacks
		self.initiative = 0                                             # turn progress from 0 to 100
		# Iteration 25: happiness (0-255) grows by battling, levelling up and walking together; extra moves
		# taught by the move tutor; bosses have three times the health
		self.happiness = 50
		self.tutored = []
		self.moves = None   # Iteration 32: the 4 moves used in battle (None = the 4 newest)
		self.boss = False
		self.abilities = MONSTER_DATA[name]['abilities']                # {unlock level: attack name}
		self.defending = False                                          # True if the monster chose 'defend' this round
		# Iteration 21: things that only last for one battle (cleared by battle_rules.end_of_battle)
		self.status = None        # 'burn', 'freeze', 'poison', 'sleep' or None
		self.status_turns = 0     # turns of sleep left
		self.stages = {}          # stat -> stage from -3 to +3 (Growl lowers attack by 1, etc.)
		self.charging = None      # (target sprite, attack) while charging a move or waiting to strike last

		# experience
		self.xp = 0                                        # experience towards the next level
		self.level_up = self.level * XP_PER_LEVEL          # experience needed for the next level
		self.evolution = MONSTER_DATA[self.name]['evolve'] # (evolved species, level) or None

		# Iteration 13
		self.nickname = None    # name the player gave the monster, or None to use the species name
		self.held_item = None   # key of HELD_ITEM_DATA, or None if the monster holds nothing
		self.shiny = False      # Iteration 16: rare different-coloured version

	# Returns a readable description of the monster, used when printing for debugging.
	def __repr__(self):
		return f'monster: {self.name}, lvl: {self.level}'

	# Returns the name to show on screen: the nickname if the player gave one, otherwise the species name.
	# The species name (self.name) is still used for looking up images and data.
	@property
	def display_name(self):
		return self.nickname if self.nickname else self.name

	# Validates and sets a nickname. Parameter: text (string). Returns True if it was accepted.
	# An empty name removes the nickname. Length check (1-12) and a check that every character is printable.
	def set_nickname(self, text):
		if not isinstance(text, str):
			return False
		name = text.strip()
		if not name:
			self.nickname = None
			return True
		if len(name) > NICKNAME_MAX_LENGTH or not name.isprintable():
			return False
		self.nickname = name
		return True

	# Returns the multiplier the held item gives for an effect ('damage', 'max_health', 'energy_cost'
	# or 'xp'), or 1 if the monster holds nothing or its item does something else.
	def held_multiplier(self, effect):
		item = HELD_ITEM_DATA.get(self.held_item)
		if item and item['effect'] == effect:
			return item['multiplier']
		return 1

	# Returns one stat scaled by the monster's level.
	# Parameter: stat (string key of base_stats, e.g. 'attack'). Returns: real number.
	# Called from: get_stats, get_base_damage, stat_limiter, battle.py, monster_index.py, main.py (nurse)
	def get_stat(self, stat):
		value = self.base_stats[stat] * self.level
		if stat == 'max_health':
			value *= self.held_multiplier('max_health')   # vital charm
			if getattr(self, 'boss', False):
				value *= 3                                    # Iteration 25: boss monsters
		if stat in ('defense', 'speed'):
			value *= self.held_multiplier(stat)           # Iteration 25: Guard Shell, Swift Scarf
		if stat in ('attack', 'defense', 'speed') and getattr(self, 'stages', None):
			value *= stage_multiplier(self.stages.get(stat, 0))   # Iteration 21: raised or lowered in battle
		return value

	# Returns a dictionary of all six stats at the current level, used by the monster index screen.
	def get_stats(self):
		return {
			'health': self.get_stat('max_health'),
			'energy': self.get_stat('max_energy'),
			'attack': self.get_stat('attack'),
			'defense': self.get_stat('defense'),
			'speed': self.get_stat('speed'),
			'recovery': self.get_stat('recovery'),
		}

	# Returns a list of the attack names this monster can use.
	# Parameter: all (Boolean) - True returns every unlocked attack; False only returns the
	# unlocked attacks the monster can currently afford with its energy (validation of energy).
	# Called from: Battle.input, Battle.draw_attacks, Battle.opponent_attack, MonsterIndex.display_main
	# Iteration 32: a monster can only use MOVE_SLOTS (4) of the moves it knows in battle. self.moves is
	# the list chosen in the Party screen; None means the 4 it learned most recently (wild and trainer monsters).
	def get_abilities(self, all = True):
		equipped = self.equipped_moves()
		if all:
			return equipped
		return [ability for ability in equipped if self.attack_cost(ability) < self.energy]

	# Every move this monster has learned so far (in the order it learned them).
	def known_moves(self):
		known = [ability for lvl, ability in sorted(self.abilities.items()) if self.level >= lvl] + list(getattr(self, 'tutored', []))
		return list(dict.fromkeys(known))   # (no repeats)

	def equipped_moves(self):
		known = self.known_moves()
		if getattr(self, 'all_moves', False):   # Iteration 33: training mode - every move can be used
			return known
		chosen = getattr(self, 'moves', None)
		if chosen is None:
			return known[-MOVE_SLOTS:]
		equipped = [move for move in chosen if move in known][:MOVE_SLOTS]
		return equipped or known[-MOVE_SLOTS:]

	# Puts a move into battle or takes it out. Returns None, or a message key if it is not allowed.
	def toggle_move(self, move):
		equipped = self.equipped_moves()
		if move in equipped:
			if len(equipped) <= 1:
				return 'moves_last'
			equipped.remove(move)
		else:
			if move not in self.known_moves():
				return 'moves_last'
			if len(equipped) >= MOVE_SLOTS:
				return 'moves_full'
			equipped.append(move)
		self.moves = equipped
		return None

	# Returns ((health, max), (energy, max), (initiative, 100)) for drawing the bars under a monster in battle.
	# Called from: MonsterStatsSprite.update
	def get_info(self):
		return (
			(self.health, self.get_stat('max_health')),
			(self.energy, self.get_stat('max_energy')),
			(self.initiative, 100)
			)

	# Subtracts the energy cost of an attack. Parameter: attack (string key of ATTACK_DATA).
	# Called from: MonsterSprite.activate_attack
	def reduce_energy(self, attack):
		self.energy -= self.attack_cost(attack)

	# Returns the energy an attack costs this monster (less if it holds a focus ring).
	def attack_cost(self, attack):
		return ATTACK_DATA[attack]['cost'] * self.held_multiplier('energy_cost')

	# Returns the raw damage of an attack before element and defence are applied:
	# attack stat * the attack's amount multiplier. Called from: MonsterSprite.animate
	def get_base_damage(self, attack):
		damage = self.get_stat('attack') * ATTACK_DATA[attack]['amount'] * self.held_multiplier('damage')
		if getattr(self, 'status', None) == 'burn':
			damage *= BURN_ATTACK   # Iteration 21: a burned monster hits for less
		return damage

	# Adds experience and levels the monster up as many times as needed.
	# Parameter: amount (int or float, must be greater than 0).
	# Iteration 6 change: the IF statement was replaced with a WHILE loop so that one large
	# reward can give more than one level (test "amount = 4000" in section 2.6).
	# Called from: Battle.award_xp
	def update_xp(self, amount):
		# type check - only numbers are accepted
		if not isinstance(amount, (int, float)) or isinstance(amount, bool):
			raise TypeError(f'xp amount must be a number, got {amount!r}')
		# range check - experience gained must be greater than 0
		if amount <= 0:
			return

		self.xp += amount * self.held_multiplier('xp')   # wise feather gives extra experience
		# keep levelling up while there is enough experience for the next level
		while self.xp >= self.level_up and self.level < MAX_LEVEL:
			self.xp -= self.level_up
			before = self.known_moves()
			self.level += 1
			self.level_up = self.level * XP_PER_LEVEL
			# Iteration 32: a new move goes straight into battle if there is a free slot, otherwise it is
			# kept spare (and the player is told, see learned_spare)
			if getattr(self, 'moves', None) is not None:
				for move in self.known_moves():
					if move not in before:
						if len(self.equipped_moves()) < MOVE_SLOTS:
							self.moves = self.equipped_moves() + [move]
						else:
							self.__dict__.setdefault('learned_spare', []).append(move)

	# Iteration 15: energy gained at the start of each of this monster's turns.
	def regain_energy(self):
		self.energy += self.get_stat('recovery') * ENERGY_PER_TURN
		self.stat_limiter()

	# Iteration 15: defending reduces damage (in Battle.apply_attack) and also gives back energy.
	def defend(self):
		self.defending = True
		self.energy += self.get_stat('max_energy') * DEFEND_ENERGY
		self.stat_limiter()

	# Range check that keeps health and energy between 0 and their maximum.
	# Runs every frame from update(), so damage, healing and the nurse can never leave invalid values.
	# Iteration 25: happiness changes, kept between 0 and 255. 'Happy' monsters (200+) sometimes hang on
	# with 1 health instead of fainting, and land critical hits a little more often.
	def change_happiness(self, amount):
		self.happiness = max(0, min(255, getattr(self, 'happiness', 50) + amount))

	def is_happy(self):
		return getattr(self, 'happiness', 50) >= 200

	def stat_limiter(self):
		self.health = max(0, min(self.health, self.get_stat('max_health')))
		self.energy = max(0, min(self.energy, self.get_stat('max_energy')))

	# Called every frame during a battle by MonsterSprite.update.
	# Parameter: dt (real) - seconds since the last frame. Increases initiative by speed * dt.
	def update(self, dt):
		self.stat_limiter()
		if not self.paused:
			self.initiative += self.get_stat('speed') * self.turn_speed * dt
