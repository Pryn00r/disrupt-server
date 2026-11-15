# settings.py
# Constants used by the whole program, kept in one place so they only need changing once.

import pygame
from pygame.math import Vector2 as vector
from os.path import abspath, dirname, join
from sys import exit

# Iteration 18: the game's main folder (the one holding audio, data and graphics), worked out from
# where this file is. Before this every path was relative to wherever Python was started from, so
# running main.py from inside the code folder crashed with "No file graphics/... found".
BASE_DIR = dirname(dirname(abspath(__file__)))

# Returns the full path of a file in the game folder, e.g. asset('graphics', 'ui', 'cross.png').
def asset(*path):
	return join(BASE_DIR, *path)

WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
FPS = 60   # Iteration 18: frame rate limit (before this the game ran flat out and used a whole CPU core)
TILE_SIZE = 64 
ANIMATION_SPEED = 6

# game details
GAME_TITLE = 'Disrupt'
SUPPORT_EMAIL = 'support.disruptgame@gmail.com' # shown on the Contact Us page

# where the player is sent, with every monster healed, if all of their monsters faint in a battle
# (map name, player start position from the Tiled map)
DEFEAT_RETURN = ('world', 'house')

# players and saves
SAVE_SLOT_COUNT = 3
USERNAME_MIN_LENGTH = 3
USERNAME_MAX_LENGTH = 12
RESERVED_USERNAMES = ('admin', 'administrator', 'moderator', 'system', 'support', 'guest')

# audio tracks controlled by the music toggle, every other sound uses the sound toggle
MUSIC_TRACKS = ('overworld', 'battle', 'gym', 'boss', 'ending',      # Iteration 18: gym, boss and ending music added
	'battle_wild', 'battle_trainer', 'zone_grass', 'zone_sand', 'zone_ice', 'zone_town')   # Iteration 19
# Iteration 19: music for each area. 'overworld' (the original track) is now only used on the menus.
MENU_MUSIC = 'overworld'
BIOME_MUSIC = {'forest': 'zone_grass', 'sand': 'zone_sand', 'ice': 'zone_ice'}
MAP_MUSIC = {'house': 'zone_town', 'hospital': 'zone_town', 'hospital2': 'zone_town',
	'plant': 'zone_grass', 'fire': 'zone_sand', 'water': 'zone_ice'}   # inside buildings and gyms
MUSIC_FADE_MS = 900
# Iteration 18: the gym leaders - beating all three ends the story
GYM_LEADERS = ('px', 'fx', 'wx')
# Iteration 19: the gym each leader is in (also the name of the spawn point outside its door on the world map)
GYM_OF_LEADER = {'px': 'plant', 'fx': 'fire', 'wx': 'water'}

# screen preferences
BRIGHTNESS_MIN, BRIGHTNESS_MAX, BRIGHTNESS_STEP = 50, 150, 10
INTRO_MODES = ('full', 'short', 'off')   # Iteration 18
AUTOSAVE_SECONDS = 180                   # Iteration 18: the game also saves itself every 3 minutes
SPRINT_SPEED = 1.7                       # Iteration 18: how much faster the player moves holding Shift
NIGHT_MODE_TINT = (165, 160, 200)

# Iteration 13
TOAST_TIME = 3.5           # seconds a message (e.g. badge earned) stays at the top of the screen
MINIMAP_SIZE = 600         # largest width/height in pixels of the full map picture
MINIMAP_HUD_SIZE = 180     # size of the corner minimap shown while walking

# Iteration 14 - accounts
PASSWORD_MIN_LENGTH, PASSWORD_MAX_LENGTH = 8, 24
PASSWORD_SYMBOLS = '!@#$%^&*()-_=+[]{};:,.?/~'      # a password needs at least one of these
SECURITY_QUESTIONS = ('question_pet', 'question_food', 'question_colour')   # text keys in localisation.py
MAX_SIGN_IN_ATTEMPTS = 5    # wrong passwords allowed before the account is locked
LOCKOUT_SECONDS = 30        # how long the account stays locked

# Iteration 14 - coins, party and battles
STARTING_COINS = 100
COINS_PER_TRAINER_LEVEL = 10    # beating a trainer gives 10 coins per level of their strongest monster
BADGE_BONUS_COINS = 100         # extra coins for beating a badge trainer the first time
RENAME_MONSTER_COST = 50        # coins to change a monster's nickname (naming the starter is free)
MAX_PARTY_SIZE = 6              # most monsters a player can keep at once
STORAGE_SIZE = 120             # Iteration 22: monsters the PC storage box can hold
# Iteration 22: how characters that are not on a sprite sheet of their own look (recoloured sheets)
NPC_LOOKS = {}   # (Iteration 22-26 gave the professor a look; the professor was removed in Iteration 27)
TURN_TIME = 1.6                 # seconds the fastest monster in a battle waits for its turn, at most

# Iteration 15 - energy. Before this a monster never got energy back during a battle, so low level
# monsters (e.g. Sparchu with 35 energy) ran out after one or two attacks and could only defend.
# Iteration 16 - shiny monsters: rare wild monsters with different colours
SHINY_CHANCE = 1 / 64           # chance that a wild monster is shiny
SHINY_HUE = 180                 # how far the colours are rotated round the colour wheel (degrees)

ENERGY_PER_TURN = 2             # energy gained at the start of each turn = recovery stat x this
DEFEND_ENERGY = 0.25            # defending also gives back this fraction of maximum energy

# colour palette - includes one colour per element so attacks and the index can be colour coded
COLORS = {
	'white': '#f4fefa', 
	'pure white': '#ffffff',
	'dark': '#2b292c',
	'light': '#c8c8c8',
	'gray': '#3a373b',
	'gold': '#ffd700',
	'light-gray': '#4b484d',
	'fire':'#f8a060',
	'water':'#50b0d8',
	'plant': '#64a990', 
	'black': '#000000', 
	'red': '#f03131',
	'blue': '#66d7ee',
	'normal': '#ffffff',
	# Iteration 21: colours for the five new types
	'ice': '#88d4ea',
	'poison': '#b064d0',
	'bug': '#a8c040',
	'flying': '#98a8f0',
	'psychic': '#f070a8',
	'rock': '#b09670',   # Iteration 27
	'ghost': '#7b6cc0', 'fairy': '#f0a0d0',   # Iteration 35 ('dark' already has a colour above)
	'dark white': '#f0f0f0'
}

# drawing order in the overworld (lower numbers are drawn first)
WORLD_LAYERS = {
	'water': 0,
	'bg': 1,
	'shadow': 2,
	'main': 3,
	'top': 4
}

# screen positions for the three monsters on each side of a battle
BATTLE_POSITIONS = {
	'left': {'top': (360, 240), 'center': (160, 390), 'bottom': (410, 545)},     # Iteration 35: spread out a little so the
	'right': {'top': (900, 240), 'center': (1130, 390), 'bottom': (900, 545)}   # name tags and stats boxes fit round them
}

# drawing order in battles
BATTLE_LAYERS =  {
	'outline': 0,
	'name': 2.5,       # Iteration 34: name tags are drawn in front of the monsters, so they are never hidden
	'monster': 2,
	'effects': 3,
	'overlay': 4
}

# icon and offset for each battle menu option. 'full' includes catch, 'limited' does not
# Iteration 16: 'run' added so the player can leave a wild battle
BATTLE_CHOICES = {
	'full': {
		'fight':  {'pos' : vector(30, -100), 'icon': 'sword'},
		'defend': {'pos' : vector(40, -60), 'icon': 'shield'},
		'items':  {'pos' : vector(45, -20), 'icon': 'bag'},     # Iteration 18: use potions during a battle
		'switch': {'pos' : vector(45, 20), 'icon': 'arrows'},
		'catch':  {'pos' : vector(40, 60), 'icon': 'hand'},
		'run':    {'pos' : vector(30, 100), 'icon': 'run'}},
	
	'limited': {
		'fight':  {'pos' : vector(30, -40), 'icon': 'sword'},
		'defend': {'pos' : vector(40, 0), 'icon': 'shield'},
		'switch': {'pos' : vector(30, 40), 'icon': 'arrows'}}
}
BATTLE_COOLDOWN = 4.0   # Iteration 25: seconds after a battle before a trainer or wild monster can start another
MOVE_SLOTS = 4   # Iteration 32: moves a monster can use in battle at once
