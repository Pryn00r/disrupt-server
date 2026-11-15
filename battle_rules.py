# battle_rules.py
# Iteration 21: the rules that decide what an attack does, kept apart from the drawing code so they can
# be tested on their own: the type chart, accuracy, priority, charge-up moves, status effects and stat
# changes. battle.py calls these functions.

from random import random, randint

from game_data import ATTACK_DATA

# attacking type -> (types it is strong against (x2), types it is weak against (x0.5))
TYPE_CHART = {
	'fire':    ({'plant', 'bug', 'ice'}, {'water', 'fire', 'rock'}),
	'water':   ({'fire', 'rock'}, {'plant'}),
	'plant':   ({'water', 'rock'}, {'fire', 'bug', 'flying', 'poison'}),
	'ice':     ({'plant', 'flying'}, {'fire', 'water'}),
	'poison':  ({'plant'}, {'poison', 'psychic', 'rock'}),
	'bug':     ({'plant', 'psychic'}, {'fire', 'flying'}),
	'flying':  ({'plant', 'bug'}, {'ice', 'rock'}),
	'psychic': ({'poison'}, {'bug', 'psychic'}),
	'normal':  (set(), {'rock'}),
	'rock':    ({'fire', 'ice', 'flying', 'bug'}, {'rock'}),   # Iteration 27: Charmadillo's second type
	# Iteration 35: move types only (no monster is dark, ghost or fairy)
	'dark':    ({'psychic', 'ghost'}, {'dark', 'fairy'}),
	'ghost':   ({'psychic', 'ghost'}, {'normal', 'dark'}),
	'fairy':   ({'dark'}, {'fire', 'poison'}),
}
TYPES = tuple(TYPE_CHART)

STATUS_EFFECTS = ('burn', 'freeze', 'poison', 'sleep', 'confused')   # Iteration 32: + confused
BURN_DAMAGE = 1 / 16      # share of max health lost at the start of each turn
POISON_DAMAGE = 1 / 10
BURN_ATTACK = 0.75        # a burned monster hits for 75%
THAW_CHANCE = 0.3         # chance a frozen monster thaws at the start of its turn
PRIORITY_HEAD_START = 45  # initiative a +1 priority move leaves the monster with (it gets its next turn sooner)
LAST_WAIT = 50            # a -1 priority move waits until initiative reaches 100 again from here
STAGE_LIMIT = 3
# Iteration 32: battles were too quick (one monster could knock another out in one hit), so all damage is
# scaled down and a super-effective hit is x1.5 per type instead of x2.
DAMAGE_SCALE = 0.6
SUPER, WEAK = 1.5, 0.67
CONFUSE_HURT = 1 / 12      # share of max health a confused monster loses when it hurts itself
CONFUSE_SELF_HIT = 0.4     # chance a confused monster hurts itself instead of acting

# Returns (multiplier, 'super' / 'weak' / None) for an attack's type against a monster's type.
# Iteration 27: a monster can have a second type; the two multipliers are multiplied together
# (so an attack strong against both types does 4 times the damage, and one that is strong against
# one and weak against the other does normal damage).
def effectiveness(attack_type, target_type, second_type = None):
	strong, weak = TYPE_CHART.get(attack_type, (set(), set()))
	multiplier = 1
	for kind in (target_type, second_type):
		if kind is None:
			continue
		if kind in strong:
			multiplier *= SUPER
		elif kind in weak:
			multiplier *= WEAK
	multiplier = round(multiplier, 2)
	if abs(multiplier - 1) < 0.05:   # one strong and one weak type cancel out (1.5 x 0.67 is about 1)
		multiplier = 1
	return multiplier, ('super' if multiplier > 1 else 'weak' if multiplier < 1 else None)

# The types of a monster: its main type and its second type (or None).
def types_of(monster):
	return monster.element, getattr(monster, 'element2', None)

def accuracy(attack):
	return ATTACK_DATA[attack].get('accuracy', 100)

# True if the attack hits. roll = a number from 0 to 1 (random unless a test passes one in).
def hits(attack, roll = None):
	return (random() if roll is None else roll) * 100 < accuracy(attack)

def priority(attack):
	return ATTACK_DATA[attack].get('priority', 0)

def is_charge(attack):
	return bool(ATTACK_DATA[attack].get('charge'))

def is_status_move(attack):
	return ATTACK_DATA[attack].get('kind') == 'status'

# Multiplier for a stat stage: +1 = x1.5, +2 = x2, -1 = x0.67, -2 = x0.5 (the same idea as the original games).
def stage_multiplier(stage):
	stage = max(-STAGE_LIMIT, min(STAGE_LIMIT, stage))
	return (2 + stage) / 2 if stage >= 0 else 2 / (2 - stage)

# Changes a monster's stat stage. Returns the change that really happened (0 if already at the limit).
def change_stage(monster, stat, change):
	old = monster.stages.get(stat, 0)
	new = max(-STAGE_LIMIT, min(STAGE_LIMIT, old + change))
	monster.stages[stat] = new
	return new - old

# Tries to give a monster a status from an attack. Returns the status given, or None.
# A monster can only have one status at a time, and a type cannot get its own status
# (fire monsters cannot burn, ice monsters cannot freeze, poison monsters cannot be poisoned).
IMMUNE = {'burn': 'fire', 'freeze': 'ice', 'poison': 'poison'}
def try_status(monster, attack, roll = None):
	effect = ATTACK_DATA[attack].get('status')
	if not effect or monster.status:
		return None
	status, chance = effect
	if IMMUNE.get(status) is not None and IMMUNE[status] in types_of(monster):
		return None
	if (random() if roll is None else roll) < chance:
		give_status(monster, status)
		return status
	return None

def give_status(monster, status):
	monster.status = status
	monster.status_turns = randint(1, 3) if status == 'sleep' else confusion_turns(monster) if status == 'confused' else 0

# Iteration 32: how many turns a monster stays confused. Monsters with a high recovery stat snap out of it
# sooner (Jacana and Finiette after about 1 turn, Pouch and Larvea after 3 or 4).
def confusion_turns(monster, extra = None):
	from game_data import MONSTER_DATA
	recovery = MONSTER_DATA[monster.name]['stats']['recovery']
	return max(1, round(5 - 2 * recovery)) + (randint(0, 1) if extra is None else extra)

# Runs a status at the start of a monster's turn. Returns (can act, message key, damage taken).
def start_of_turn(monster, roll = None):
	status = monster.status
	if status in ('burn', 'poison'):
		damage = monster.get_stat('max_health') * (BURN_DAMAGE if status == 'burn' else POISON_DAMAGE)
		monster.health -= damage
		return True, f'status_hurt_{status}', damage
	if status == 'freeze':
		if (random() if roll is None else roll) < THAW_CHANCE:
			monster.status = None
			return True, 'status_thawed', 0
		return False, 'status_frozen', 0
	if status == 'sleep':
		monster.status_turns -= 1
		if monster.status_turns < 0:
			monster.status = None
			return True, 'status_woke', 0
		return False, 'status_asleep', 0
	if status == 'confused':
		monster.status_turns -= 1
		if monster.status_turns < 0:
			monster.status = None
			return True, 'status_unconfused', 0
		if (random() if roll is None else roll) < CONFUSE_SELF_HIT:
			damage = monster.get_stat('max_health') * CONFUSE_HURT
			monster.health -= damage
			return False, 'status_confused_hurt', damage
		return True, 'status_confused', 0
	return True, None, 0

# Everything a battle changes is cleared when it ends (statuses, stat changes, a charging move).
def end_of_battle(monster):
	monster.status, monster.status_turns, monster.stages, monster.charging = None, 0, {}, None

# Iteration 34: how big a move's animation is drawn. Status and healing moves are normal size; attacks get
# bigger with their power (power 1 = normal size, power 3 = one and a half times as big).
def animation_scale(attack):
	data = ATTACK_DATA[attack]
	if 'scale' in data:   # Iteration 35: a few moves are drawn extra big (Venom Burst, Dark Pulse, Sleep Spores)
		return data['scale']
	if data.get('kind') in ('status', 'heal') or not data['amount']:
		return 0.9
	return max(0.85, min(1.6, 0.75 + 0.25 * data['amount']))

# Iteration 34: a move's power as a whole number for the menus (1.2 -> 60). None for moves that do no damage.
def move_power(attack):
	data = ATTACK_DATA[attack]
	if data.get('kind') in ('status', 'heal') or not data['amount']:
		return None
	return round(data['amount'] * 50)
