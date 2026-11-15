# game_data.py
# All of the game's content is stored here as dictionaries, separate from the code that uses it.

# TRAINER_DATA: key = character_id from the Tiled map. monsters: {position: (species, level)},
# dialog: lines before/after being beaten - a line written as ('player', text) is said by the player
# instead of the trainer (Iteration 14), directions: where they look, look_around: whether they can
# spot the player, defeated: becomes True after the battle, biome: battle background
# Levels were rebalanced (Iteration 13) so the game starts easy next to the house and gets harder
# towards the gyms: beach -> plant gym (about 16-23) -> fire gym (about 22-33) -> water gym (about 32-45).
TRAINER_DATA = {
	'o1': {
		'monsters': {0: ('Larvea', 3)},   # Iteration 15: one weak monster so the tutorial battle is fair
		'dialog': {
			'default': ['Oi! You! New around here?', ('player', 'Uh... one minute I was playing a game, now I am IN it?!'), "Perfect. Fresh meat! Let's battle!", ('player', "I really don't want to fight."), 'Too late, my Larvea has already stretched.', 'FIGHT!'],
			'defeated': ['Okay, okay... my Larvea needs a nap. So do I.', 'The girls on the beach are tougher than me. Go bother them.']},
		'directions': ['down'],
		'look_around': True,
		'defeated': False,
		'biome': 'forest'
		},
	'o2': {
		'monsters': {0: ('Cleaf', 6)},
		'dialog': {
			'default': ["I don't like sand.", "It's coarse and rough and it gets everywhere.", ('player', '...then why are you on a beach?'), "Don't question me. FIGHT!"],
			'defeated': ['Ugh. Sand in my shoes AND I lost.', 'Train in the sand patches if you want stronger monsters.']},
		'directions': ['left', 'down'],
		'look_around': False,
		'defeated': False,
		'biome': 'sand'
		},
	'o3': {
		'monsters': {0: ('Pouch', 5)},   # Iteration 15: one monster each on the beach - the player only has a starter
		'dialog': {
			'default': ["Hey! You're blocking my sun.", ('player', "It's a beach. There is sun everywhere."), 'Not where YOU are standing. Battle me for it!'],
			'defeated': ['Fine. Keep the sun.', 'The blonde girl down the beach is way more competitive than me.']},
		'directions': ['left', 'right', 'up', 'down'],
		'look_around': True,
		'defeated': False,
		'biome': 'sand'
		},
	'o4': {
		'monsters': {0: ('Cindrill', 13), 1: ('Gulfin', 12), 2: ('Atrox', 14)},
		'dialog': {
			'default': ["Shh! I'm birdwatching.", ('player', "There aren't any birds."), 'Because YOU scared them off! Battle!'],
			'defeated': ['...I think I just saw a pigeon. Worth it.', 'The Plant Gym is north, past the trees.']},
		'directions': ['right'],
		'look_around': True,
		'defeated': False,
		'biome': 'forest'
		},
	'o5': {
		'monsters': {0: ('Ivieron', 15), 1: ('Pouch', 16), 2: ('Atrox', 15)},
		'dialog': {
			'default': ['So you want to challenge the big ones?', ('player', 'The big what?'), 'The GYMS! Prove yourself to me first.'],
			'defeated': ["Okay, you're ready. The Plant Gym is right behind me.", 'Mind the vines. They bite.']},
		'directions': ['up', 'right'],
		'look_around': True,
		'defeated': False,
		'biome': 'forest'
		},
	'o6': {
		'monsters': {0: ('Finsta', 20), 1: ('Gulfin', 22), 2: ('Friolera', 22)},
		'dialog': {
			'default': ['Do you smell smoke?', ('player', "That's probably the Fire Gym right next to you."), 'Oh. Right. Anyway, fight me!'],
			'defeated': ['Too hot to lose today... and yet I did.', 'Bring water monsters into that gym. Trust me.']},
		'directions': ['down'],
		'look_around': False,
		'defeated': False,
		'biome': 'sand'   # Iteration 19: was 'ice', but this trainer stands in the desert next to the Fire Gym
		},
	'o7': {
		'monsters': {0: ('Friolera', 30), 1: ('Gulfin', 32), 2: ('Draem', 31)},
		'dialog': {
			'default': ['Hey! Wanna build a snowman?', ('player', 'Sure!'), "Too bad, we're battling instead!"],
			'defeated': ['My snowman would have won.', 'The Water Gym is up north. Wrap up warm!']},
		'directions': ['right'],
		'look_around': False,
		'defeated': False,
		'biome': 'ice'
		},
	'p1': {
		'monsters': {0: ('Plumette', 16), 1: ('Pouch', 16)},
		'dialog': {
			'default': ['Welcome to the Plant Gym!', "Rule one: don't step on the flowers.", ('player', "I haven't touched any flowers."), 'Rule two: we battle anyway!'],
			'defeated': ['You stepped on SO many flowers.', 'The leader is at the top. Good luck!']},
		'directions': ['down'],   # Iteration 32: was ['right'] (everyone faced right)
		'look_around': False,
		'defeated': False,
		'biome': 'forest'
		},
	'p2': {
		'monsters': {0: ('Ivieron', 17), 1: ('Cleaf', 17)},
		'dialog': {
			'default': ['Are you lost? This maze is made of hedges.', ('player', "I'm not lost, I'm exploring."), "That's what lost people say. Fight!"],
			'defeated': ['Okay, you might not be lost.']},
		'directions': ['down'],   # Iteration 32: was ['right'] (everyone faced right)
		'look_around': False,
		'defeated': False,
		'biome': 'forest'
		},
	'p3': {
		'monsters': {0: ('Larvea', 17), 1: ('Draem', 18)},
		'dialog': {
			'default': ['I talk to my plants every day.', ('player', 'Do they talk back?'), 'Only when they want to battle!'],
			'defeated': ['My plants say well done.']},
		'directions': ['left'],   # Iteration 32: was ['right'] (everyone faced right)
		'look_around': False,
		'defeated': False,
		'biome': 'forest'
		},
	'p4': {
		'monsters': {0: ('Pouch', 18), 1: ('Ivieron', 18)},
		'dialog': {
			'default': ['Leaf me alone!', ('player', "I didn't even say anything."), '...Fine. Battle!'],
			'defeated': ['That was a tree-mendous battle.']},
		'directions': ['down'],   # Iteration 32: was ['right'] (everyone faced right)
		'look_around': False,
		'defeated': False,
		'biome': 'forest'
		},
	'px': {
		'monsters': {0: ('Ivieron', 20), 1: ('Draem', 21), 2: ('Pouch', 21), 3: ('Pluma', 23)},
		'dialog': {
			'default': ['Welcome to my garden, challenger.', 'Only those who grow may pass.', ('player', 'Did you just make a plant pun?'), 'Leaf the jokes to me. FIGHT!'],
			'defeated': ["You've really blossomed.", 'Take the Leaf Badge. Two more and this world will let you go.']},
		'directions': ['down'],   # Iteration 32: was ['right'] (everyone faced right)
		'look_around': False,
		'defeated': False,
		'biome': 'forest'
		},
	'w1': {
		'monsters': {0: ('Finsta', 32), 1: ('Friolera', 32)},
		'dialog': {
			'default': ["It's so cold in here.", ('player', "It's a water gym in the snow. What did you expect?"), 'Maybe a fight will warm me up!'],
			'defeated': ['Still cold. Still lost.']},
		'directions': ['left'],
		'look_around': True,
		'defeated': False,
		'biome': 'ice'
		},
	'w2': {
		'monsters': {0: ('Gulfin', 33), 1: ('Friolera', 33)},
		'dialog': {
			'default': ['I came here from the beach!', ('player', "Wait, haven't I already beaten you?"), 'That was my twin sister. FIGHT!'],
			'defeated': ["Don't tell my sister about this."]},
		'directions': ['right'],
		'look_around': True,
		'defeated': False,
		'biome': 'ice'
		},
	'w3': {
		'monsters': {0: ('Gulfin', 34), 1: ('Draem', 34)},
		'dialog': {
			'default': ['Slipping on the ice is part of the training.', ('player', 'That sounds painful.'), 'It is! Battle!'],
			'defeated': ['Ouch. In more ways than one.']},
		'directions': ['right'],
		'look_around': True,
		'defeated': False,
		'biome': 'ice'
		},
	'w4': {
		'monsters': {0: ('Friolera', 35), 1: ('Gulfin', 35)},
		'dialog': {
			'default': ['I built an igloo in here.', ('player', 'Indoors?'), 'Indoors! Now fight!'],
			'defeated': ['You can visit my igloo any time.']},
		'directions': ['left'],
		'look_around': True,
		'defeated': False,
		'biome': 'ice'
		},
	'w5': {
		'monsters': {0: ('Draem', 36), 1: ('Gulfin', 36)},
		'dialog': {
			'default': ['Only the leader is left after me.', ('player', 'Then let me through!'), 'Not without a battle!'],
			'defeated': ['Go. The leader is waiting.']},
		'directions': ['right'],
		'look_around': True,
		'defeated': False,
		'biome': 'ice'
		},
	'wx': {
		'monsters': {0: ('Gulfin', 38), 1: ('Friolera', 38), 2: ('Draem', 39), 3: ('Finiette', 45)},
		'dialog': {
			'default': ['So you made it through the snow.', ('player', 'My toes are frozen.'), "Then let's warm up with the final battle!"],
			'defeated': ['The tide has turned.', 'Take the Tide Badge. Three badges... the way out is open.']},
		'directions': ['down'],
		'look_around': False,
		'defeated': False,
		'biome': 'ice'
		},
	'f1': {
		'monsters': {0: ('Cindrill', 22), 1: ('Jacana', 22)},
		'dialog': {
			'default': ['Welcome to the Fire Gym!', ('player', "It's like 40 degrees in here."), "That's the point! FIGHT!"],
			'defeated': ["You're on fire! ...Not literally. Hopefully."]},
		'directions': ['right'],
		'look_around': True,
		'defeated': False,
		'biome': 'sand'
		},
	'f2': {
		'monsters': {0: ('Atrox', 23), 1: ('Cindrill', 23)},
		'dialog': {
			'default': ["I've been waiting by this lava all day.", ('player', 'Why?'), 'For someone to battle! Finally!'],
			'defeated': ['Worth the wait.']},
		'directions': ['right', 'left'],
		'look_around': False,
		'defeated': False,
		'biome': 'sand'
		},
	'f3': {
		'monsters': {0: ('Jacana', 24), 1: ('Atrox', 24)},
		'dialog': {
			'default': ['My monsters are hot-headed today.', ('player', "Is that why there's smoke coming out of them?"), 'FIGHT!'],
			'defeated': ['Everyone, cool down. We lost.']},
		'directions': ['right', 'left'],
		'look_around': True,
		'defeated': False,
		'biome': 'sand'
		},
	'f4': {
		'monsters': {0: ('Cindrill', 25), 1: ('Jacana', 25)},
		'dialog': {
			'default': ['Do you even have a fire monster?', ('player', 'Does it matter?'), 'Not really. Battle!'],
			'defeated': ["Okay, it really didn't matter."]},
		'directions': ['up', 'right'],
		'look_around': True,
		'defeated': False,
		'biome': 'sand'
		},
	'f5': {
		'monsters': {0: ('Atrox', 25), 1: ('Cindrill', 26)},
		'dialog': {
			'default': ["I bet you can't take the heat!", ('player', "I've taken the heat from four people already."), 'Make it five!'],
			'defeated': ['Make it... five losses for me.']},
		'directions': ['left'],
		'look_around': True,
		'defeated': False,
		'biome': 'sand'
		},
	'f6': {
		'monsters': {0: ('Jacana', 26), 1: ('Atrox', 26)},
		'dialog': {
			'default': ['The boss is just behind me.', ('player', 'So can I go past?'), 'Only if you beat me!'],
			'defeated': ['Go on then. Bring a fan.']},
		'directions': ['right'],
		'look_around': True,
		'defeated': False,
		'biome': 'sand'
		},
	'fx': {
		'monsters': {0: ('Cindrill', 28), 1: ('Atrox', 28), 2: ('Jacana', 29), 3: ('Charmadillo', 33)},
		'dialog': {
			'default': ['Time to bring the heat!', ('player', 'Everyone here keeps saying that.'), "Because it's TRUE! FIGHT!"],
			'defeated': ['You put out my flames...', 'The Flame Badge is yours. One gym left, then you can leave.']},
		'directions': ['down'],
		'look_around': False,
		'defeated': False,
		'biome': 'sand'
		},
	'Nurse': {
		'direction': 'down',
		'radius': 0,
		'look_around': False,
		'dialog': {
			'default': ['Welcome to the hospital!', 'Your monsters are all healed up.', 'Have a look at my shop before you go.'], 
			'defeated': None},
		'directions': ['down'],
		'defeated': False,
		'biome': None
		}
}

# MONSTER_DATA: key = species. stats are level 1 values (multiplied by level in get_stat),
# abilities = {unlock level: attack}, evolve = (species, level) or None
MONSTER_DATA = {
	'Plumette': {
		'stats': {'element': 'plant', 'max_health': 16, 'max_energy': 17, 'attack': 4, 'defense': 8, 'recovery': 1.2, 'speed': 2},   # Iteration 15: starters made faster
		'abilities': {0: 'scratch', 3: 'vine whip', 7: 'seed shot', 10: 'petal spit', 12: 'sleep spores', 16: 'grassy heal', 20: 'leaf storm', 28: 'solar beam'},
		'evolve': ('Ivieron', 15)},
	'Ivieron': {
		'stats': {'element': 'plant', 'element2': 'poison', 'max_health': 18, 'max_energy': 20, 'attack': 5, 'defense': 10, 'recovery': 1.2, 'speed': 1.2},
		'abilities': {0: 'scratch', 3: 'vine whip', 7: 'seed shot', 10: 'petal spit', 12: 'sleep spores', 16: 'grassy heal', 20: 'leaf storm', 28: 'solar beam'},
		'evolve': ('Pluma', 32)},
	'Pluma': {
		'stats': {'element': 'plant', 'element2': 'poison', 'max_health': 23, 'max_energy': 26, 'attack': 6, 'defense': 12, 'recovery': 1.8, 'speed': 1.8},
		'abilities': {0: 'scratch', 3: 'vine whip', 7: 'seed shot', 10: 'petal spit', 12: 'sleep spores', 16: 'grassy heal', 20: 'leaf storm', 28: 'solar beam'},
		'evolve': None},
	'Sparchu': {
		'stats': {'element': 'fire', 'max_health': 16, 'max_energy': 10, 'attack': 4, 'defense': 8, 'recovery': 1.2, 'speed': 2},
		'abilities': {0: 'scratch', 3: 'spark', 7: 'ember dash', 10: 'power up', 12: 'burn', 15: 'fire pillar', 18: 'fire', 26: 'explosion'},
		'evolve': ('Cindrill', 15)},
	'Cindrill': {
		'stats': {'element': 'fire', 'max_health': 18, 'max_energy': 10, 'attack': 3.5, 'defense': 10, 'recovery': 1.2, 'speed': 1.1},
		'abilities': {0: 'scratch', 3: 'spark', 7: 'ember dash', 10: 'power up', 12: 'burn', 15: 'fire pillar', 18: 'fire', 26: 'explosion'},
		'evolve': ('Charmadillo', 33)},
	'Charmadillo': {
		'stats': {'element': 'fire', 'element2': 'rock', 'max_health': 29, 'max_energy': 12, 'attack': 4, 'defense': 17, 'recovery': 1.35, 'speed': 1.1},
		'abilities': {0: 'scratch', 3: 'spark', 7: 'ember dash', 10: 'power up', 12: 'burn', 15: 'fire pillar', 18: 'fire', 22: 'rock throw', 26: 'explosion', 30: 'inferno', 40: 'annihilate'},
		'evolve': None},
	'Finsta': {
		'stats': {'element': 'water', 'max_health': 13, 'max_energy': 17, 'attack': 3.5, 'defense': 8, 'recovery': 1.5, 'speed': 2.2},
		'abilities': {0: 'scratch', 3: 'bubble', 7: 'aqua jet', 9: 'guard up', 12: 'soak', 14: 'heal', 18: 'splash', 25: 'tidal wave'},
		'evolve': ('Gulfin', 34)},
	'Gulfin': {
		'stats': {'element': 'water', 'max_health': 18, 'max_energy': 20, 'attack': 3, 'defense': 10, 'recovery': 1.8, 'speed': 2},
		'abilities': {0: 'scratch', 3: 'bubble', 7: 'aqua jet', 9: 'guard up', 12: 'soak', 14: 'heal', 18: 'splash', 25: 'tidal wave', 32: 'ice'},
		'evolve': ('Finiette', 45)},
	'Finiette': {
		'stats': {'element': 'water', 'element2': 'ice', 'max_health': 27, 'max_energy': 23, 'attack': 4, 'defense': 17, 'recovery': 2, 'speed': 2.5},
		'abilities': {0: 'scratch', 3: 'bubble', 7: 'aqua jet', 9: 'guard up', 12: 'soak', 14: 'heal', 18: 'splash', 25: 'tidal wave', 32: 'ice'},
		'evolve': None},
	'Atrox': {
		'stats': {'element': 'poison', 'max_health': 18, 'max_energy': 20, 'attack': 3, 'defense': 10, 'recovery': 1.3, 'speed': 1.9},
		'abilities': {0: 'poison sting', 4: 'acid flick', 6: 'acid spray', 9: 'toxic', 11: 'glare', 14: 'bug bite', 20: 'venom burst'},
		'evolve': None},
	'Pouch': {
		'stats': {'element': 'normal', 'max_health': 23, 'max_energy': 25, 'attack': 4, 'defense': 12, 'recovery': 1, 'speed': 1.5},
		'abilities': {0: 'tackle', 3: 'growl', 5: 'glare', 6: 'quick strike', 8: 'headbutt', 12: 'vine whip', 14: 'heal', 18: 'mega charge', 20: 'power up'},
		'evolve': None},
	'Draem': {
		'stats': {'element': 'psychic', 'max_health': 23, 'max_energy': 25, 'attack': 4, 'defense': 12, 'recovery': 1.2, 'speed': 1.4},
		'abilities': {0: 'mind pulse', 4: 'blink', 7: 'confuse ray', 9: 'hypnosis', 12: 'dark pulse', 16: 'bubble', 20: 'nightmare', 22: 'future sight'},
		'evolve': None},
	'Larvea': {
		'stats': {'element': 'bug', 'max_health': 15, 'max_energy': 17, 'attack': 1, 'defense': 8, 'recovery': 1, 'speed': 1},
		'abilities': {0: 'bug bite', 3: 'silk trap', 5: 'acid spray'},
		'evolve': ('Cleaf', 4)},
	'Cleaf': {
		'stats': {'element': 'bug', 'element2': 'plant', 'max_health': 18, 'max_energy': 20, 'attack': 3, 'defense': 10, 'recovery': 1.7, 'speed': 1.6},
		'abilities': {0: 'bug bite', 3: 'silk trap', 5: 'acid spray', 6: 'swarm rush', 9: 'acid pool', 12: 'vine whip', 18: 'megahorn'},
		'evolve': None},
	'Jacana': {
		'stats': {'element': 'flying', 'max_health': 12, 'max_energy': 19, 'attack': 3, 'defense': 10, 'recovery': 2.1, 'speed': 2.6},
		'abilities': {0: 'peck', 3: 'wing dart', 5: 'static shock', 8: 'feather dance', 14: 'spark', 16: 'thunder', 20: 'sky dive', 26: 'storm call'},
		'evolve': None},
	'Friolera': {
		'stats': {'element': 'ice', 'max_health': 13, 'max_energy': 20, 'attack': 4, 'defense': 6, 'recovery': 1.3, 'speed': 2},
		'abilities': {0: 'frost bite', 4: 'ice shard', 6: 'glare', 8: 'ice', 12: 'headbutt', 15: 'soak', 18: 'heal', 22: 'blizzard'},
		'evolve': None},
}

# ATTACK_DATA: target ('opponent' or own side 'player'), amount (damage multiplier, negative heals),
# cost (energy), element and animation
ATTACK_DATA = {
	'rock throw':    {'target': 'opponent', 'amount': 1.5, 'cost': 18, 'element': 'rock',    'animation': 'rock_throw', 'accuracy': 90},   # Iteration 27
	# Iteration 21: every attack can also have
	#   priority  +1 = acts straight away and gets the next turn sooner, -1 = waits and strikes last
	#   accuracy  chance to hit in % (100 if not given)
	#   charge    True = charges for one turn, then hits on the next
	#   status    (effect, chance) - 'burn', 'freeze', 'poison' or 'sleep'
	#   stat      (stat, change) - lowers ('attack', -1) or raises a stat for the rest of the battle
	#   kind      'status' for moves that do no damage
	# the moves from before Iteration 21
	'scratch':    {'target': 'opponent', 'amount': 1.2,  'cost': 20, 'element': 'normal', 'animation': 'scratch'},
	'spark':      {'target': 'opponent', 'amount': 1.1,  'cost': 12, 'element': 'fire',   'animation': 'spark', 'sound': 'fire'},
	'burn':       {'target': 'opponent', 'amount': 2,    'cost': 15, 'element': 'fire',   'animation': 'burn', 'sound': 'fire', 'status': ('burn', 0.3)},
	'fire':       {'target': 'opponent', 'amount': 2,    'cost': 15, 'element': 'fire',   'animation': 'fire'},
	'explosion':  {'target': 'opponent', 'amount': 2,    'cost': 90, 'element': 'fire',   'animation': 'explosion'},
	'annihilate': {'target': 'opponent', 'amount': 3,    'cost': 30, 'element': 'fire',   'animation': 'annihilate', 'accuracy': 80, 'sound': 'explosion'},
	'splash':     {'target': 'opponent', 'amount': 2,    'cost': 15, 'element': 'water',  'animation': 'splash'},
	'ice':        {'target': 'opponent', 'amount': 2,    'cost': 15, 'element': 'ice',    'animation': 'ice', 'status': ('freeze', 0.2)},
	'vine whip':  {'target': 'opponent', 'amount': 1.4,  'cost': 12, 'element': 'plant',  'animation': 'vine'},   # Iteration 32: the Plants pack vine
	'leaf storm': {'target': 'opponent', 'amount': 2.4,  'cost': 28, 'element': 'plant',  'animation': 'green'},
	'bubble':     {'target': 'opponent', 'amount': 1.4,  'cost': 12, 'element': 'water',  'animation': 'bubble', 'sound': 'splash'},
	'tidal wave': {'target': 'opponent', 'amount': 2.4,  'cost': 28, 'element': 'water',  'animation': 'tidal_wave', 'sound': 'splash'},
	# Iteration 21: four moves for every type - a basic hit, a priority move, a status move and a big move
	'tackle':        {'target': 'opponent', 'amount': 1.2, 'cost': 10, 'element': 'normal',  'animation': 'tackle'},
	'quick strike':  {'target': 'opponent', 'amount': 0.9, 'cost': 12, 'element': 'normal',  'animation': 'quick', 'priority': 1},
	'growl':         {'target': 'opponent', 'amount': 0,   'cost': 10, 'element': 'normal',  'animation': 'growl', 'kind': 'status', 'stat': ('attack', -1)},
	'mega charge':   {'target': 'opponent', 'amount': 3.0, 'cost': 30, 'element': 'normal',  'animation': 'mega', 'charge': True},
	'ember dash':    {'target': 'opponent', 'amount': 1.0, 'cost': 14, 'element': 'fire',    'animation': 'ember', 'priority': 1, 'status': ('burn', 0.1)},
	'aqua jet':      {'target': 'opponent', 'amount': 1.0, 'cost': 14, 'element': 'water',   'animation': 'aqua', 'priority': 1},
	'soak':          {'target': 'opponent', 'amount': 0,   'cost': 12, 'element': 'water',   'animation': 'soak', 'kind': 'status', 'stat': ('speed', -1)},
	'seed shot':     {'target': 'opponent', 'amount': 1.0, 'cost': 14, 'element': 'plant',   'animation': 'seed', 'priority': 1},
	'sleep spores':  {'target': 'opponent', 'amount': 0,   'cost': 18, 'element': 'plant',   'animation': 'spores', 'kind': 'status', 'status': ('sleep', 1.0), 'accuracy': 80},
	'solar beam':    {'target': 'opponent', 'amount': 3.0, 'cost': 30, 'element': 'plant',   'animation': 'solar', 'charge': True},
	'frost bite':    {'target': 'opponent', 'amount': 1.3, 'cost': 12, 'element': 'ice',     'animation': 'frost', 'status': ('freeze', 0.1)},
	'ice shard':     {'target': 'opponent', 'amount': 1.0, 'cost': 14, 'element': 'ice',     'animation': 'shard', 'priority': 1},
	'blizzard':      {'target': 'opponent', 'amount': 2.6, 'cost': 30, 'element': 'ice',     'animation': 'blizzard', 'status': ('freeze', 0.25), 'accuracy': 75},
	'poison sting':  {'target': 'opponent', 'amount': 1.2, 'cost': 12, 'element': 'poison',  'animation': 'sting', 'status': ('poison', 0.3)},
	'acid flick':    {'target': 'opponent', 'amount': 1.0, 'cost': 14, 'element': 'poison',  'animation': 'acid', 'priority': 1},
	'toxic':         {'target': 'opponent', 'amount': 0,   'cost': 16, 'element': 'poison',  'animation': 'toxic', 'kind': 'status', 'status': ('poison', 1.0), 'accuracy': 90},
	'venom burst':   {'target': 'opponent', 'amount': 2.5, 'cost': 28, 'element': 'poison',  'animation': 'venom'},
	'bug bite':      {'target': 'opponent', 'amount': 1.3, 'cost': 12, 'element': 'bug',     'animation': 'bite'},
	'swarm rush':    {'target': 'opponent', 'amount': 1.0, 'cost': 14, 'element': 'bug',     'animation': 'swarm', 'priority': 1},
	'silk trap':     {'target': 'opponent', 'amount': 0,   'cost': 12, 'element': 'bug',     'animation': 'silk', 'kind': 'status', 'stat': ('speed', -1)},
	'megahorn':      {'target': 'opponent', 'amount': 2.8, 'cost': 28, 'element': 'bug',     'animation': 'horn', 'accuracy': 80},
	'peck':          {'target': 'opponent', 'amount': 1.2, 'cost': 10, 'element': 'flying',  'animation': 'peck'},
	'wing dart':     {'target': 'opponent', 'amount': 1.0, 'cost': 14, 'element': 'flying',  'animation': 'wing', 'priority': 1},
	'feather dance': {'target': 'opponent', 'amount': 0,   'cost': 12, 'element': 'flying',  'animation': 'feather', 'kind': 'status', 'stat': ('attack', -1)},
	'sky dive':      {'target': 'opponent', 'amount': 3.0, 'cost': 30, 'element': 'flying',  'animation': 'dive', 'charge': True},
	'mind pulse':    {'target': 'opponent', 'amount': 1.3, 'cost': 12, 'element': 'psychic', 'animation': 'mind'},
	'blink':         {'target': 'opponent', 'amount': 1.0, 'cost': 14, 'element': 'psychic', 'animation': 'blink', 'priority': 1},
	'hypnosis':      {'target': 'opponent', 'amount': 0,   'cost': 18, 'element': 'psychic', 'animation': 'hypno', 'kind': 'status', 'status': ('sleep', 1.0), 'accuracy': 75},
	'future sight':  {'target': 'opponent', 'amount': 3.0, 'cost': 30, 'element': 'psychic', 'animation': 'future', 'charge': True},
	# Iteration 32: new moves with the new animations. Also used here:
	#   kind 'heal'   heals one of your own monsters by 'heal' x its maximum health (target 'player')
	#   stat_chance   chance that a damaging move's stat change happens (1 if not given)
	#   self_status   (effect, chance) - the attacker can get this status too (Headbutt makes both dizzy)
	#   'confused' is a status: a confused monster may hurt itself instead of acting, for a few turns
	'heal':          {'target': 'player',   'amount': 0,   'cost': 20, 'element': 'normal',  'animation': 'heal_aura', 'kind': 'heal', 'heal': 0.35},
	'headbutt':      {'target': 'opponent', 'amount': 1.5, 'cost': 16, 'element': 'normal',  'animation': 'confused', 'status': ('confused', 0.5), 'self_status': ('confused', 0.4), 'accuracy': 90},
	'glare':         {'target': 'opponent', 'amount': 0,   'cost': 10, 'element': 'normal',  'animation': 'glare', 'kind': 'status', 'stat': ('defense', -1)},
	'power up':      {'target': 'player',   'amount': 0,   'cost': 14, 'element': 'normal',  'animation': 'power_up', 'kind': 'status', 'stat': ('attack', 1)},
	'guard up':      {'target': 'player',   'amount': 0,   'cost': 14, 'element': 'normal',  'animation': 'guard_up', 'kind': 'status', 'stat': ('defense', 1)},
	'fire pillar':   {'target': 'opponent', 'amount': 2.0, 'cost': 22, 'element': 'fire',    'animation': 'fire_pillar', 'stat': ('defense', -1), 'stat_chance': 0.3},
	'inferno':       {'target': 'opponent', 'amount': 3.0, 'cost': 32, 'element': 'fire',    'animation': 'inferno', 'status': ('burn', 0.3), 'accuracy': 90, 'charge': True},
	'static shock':  {'target': 'opponent', 'amount': 1.2, 'cost': 14, 'element': 'flying',  'animation': 'static', 'stat': ('speed', -1), 'stat_chance': 0.4},
	'thunder':       {'target': 'opponent', 'amount': 2.2, 'cost': 24, 'element': 'flying',  'animation': 'thunder', 'accuracy': 90},
	'storm call':    {'target': 'opponent', 'amount': 2.8, 'cost': 32, 'element': 'flying',  'animation': 'storm', 'accuracy': 80, 'status': ('confused', 0.2)},
	'acid spray':    {'target': 'opponent', 'amount': 1.1, 'cost': 12, 'element': 'bug',     'animation': 'acid_spray', 'status': ('poison', 0.25)},
	'acid pool':     {'target': 'opponent', 'amount': 1.6, 'cost': 18, 'element': 'bug',     'animation': 'acid_pool', 'stat': ('defense', -1), 'stat_chance': 0.5},
	'confuse ray':   {'target': 'opponent', 'amount': 0,   'cost': 14, 'element': 'psychic', 'animation': 'confuse_ray', 'kind': 'status', 'status': ('confused', 0.9)},
	'dark pulse':    {'target': 'opponent', 'amount': 1.6, 'cost': 18, 'element': 'psychic', 'animation': 'dark_pulse', 'stat': ('attack', -1), 'stat_chance': 0.3},
	'nightmare':     {'target': 'opponent', 'amount': 2.4, 'cost': 28, 'element': 'psychic', 'animation': 'nightmare', 'status': ('sleep', 0.15)},
	'petal spit':    {'target': 'opponent', 'amount': 1.3, 'cost': 14, 'element': 'plant',   'animation': 'petal', 'stat': ('attack', -1), 'stat_chance': 0.3},
	'grassy heal':   {'target': 'player',   'amount': 0,   'cost': 18, 'element': 'plant',   'animation': 'grass_grow', 'kind': 'heal', 'heal': 0.3},
	# Iteration 33: one move for every animation left in the packs (mostly the Super Pixel Effects Gigapack)
	# normal
	'body slam':     {'target': 'opponent', 'amount': 1.6, 'cost': 18, 'element': 'normal',  'animation': 'body_slam', 'stat': ('speed', -1), 'stat_chance': 0.3},
	'hyper blast':   {'target': 'opponent', 'amount': 3.2, 'cost': 34, 'element': 'normal',  'animation': 'hyper_blast', 'charge': True, 'accuracy': 90},
	'coin toss':     {'target': 'opponent', 'amount': 1.0, 'cost': 8,  'element': 'normal',  'animation': 'coin_toss'},
	'sing':          {'target': 'opponent', 'amount': 0,   'cost': 16, 'element': 'normal',  'animation': 'sing', 'kind': 'status', 'status': ('sleep', 1.0), 'accuracy': 70},
	'charm':         {'target': 'opponent', 'amount': 0,   'cost': 12, 'element': 'normal',  'animation': 'charm', 'kind': 'status', 'stat': ('attack', -2)},
	'focus energy':  {'target': 'player',   'amount': 0,   'cost': 22, 'element': 'normal',  'animation': 'focus', 'kind': 'status', 'stat': ('attack', 2)},
	'scary face':    {'target': 'opponent', 'amount': 0,   'cost': 10, 'element': 'normal',  'animation': 'scary_face', 'kind': 'status', 'stat': ('speed', -2)},
	'taunt':         {'target': 'opponent', 'amount': 0,   'cost': 10, 'element': 'normal',  'animation': 'taunt', 'kind': 'status', 'stat': ('defense', -2)},
	'smokescreen':   {'target': 'opponent', 'amount': 0,   'cost': 12, 'element': 'normal',  'animation': 'smoke', 'kind': 'status', 'status': ('confused', 0.6)},
	'agility':       {'target': 'player',   'amount': 0,   'cost': 14, 'element': 'normal',  'animation': 'agility', 'kind': 'status', 'stat': ('speed', 2)},
	'riddle':        {'target': 'opponent', 'amount': 0.8, 'cost': 12, 'element': 'normal',  'animation': 'riddle', 'status': ('confused', 0.4)},
	'war cry':       {'target': 'player',   'amount': 0,   'cost': 8,  'element': 'normal',  'animation': 'war_cry', 'kind': 'status', 'stat': ('attack', 1), 'priority': 1},
	# fire
	'flame wheel':   {'target': 'opponent', 'amount': 1.4, 'cost': 14, 'element': 'fire',    'animation': 'flame_wheel', 'priority': 1, 'status': ('burn', 0.1)},
	'blue flame':    {'target': 'opponent', 'amount': 0,   'cost': 16, 'element': 'fire',    'animation': 'blue_flame', 'kind': 'status', 'status': ('burn', 1.0), 'accuracy': 85},
	'heat wave':     {'target': 'opponent', 'amount': 2.0, 'cost': 22, 'element': 'fire',    'animation': 'heat_wave', 'stat': ('speed', -1), 'stat_chance': 0.3},
	'flame burst':   {'target': 'opponent', 'amount': 1.8, 'cost': 20, 'element': 'fire',    'animation': 'flame_burst', 'stat': ('defense', -1), 'stat_chance': 0.2},
	'firework':      {'target': 'opponent', 'amount': 1.5, 'cost': 16, 'element': 'fire',    'animation': 'firework', 'status': ('confused', 0.2)},
	'spark shower':  {'target': 'opponent', 'amount': 1.2, 'cost': 12, 'element': 'fire',    'animation': 'spark_shower', 'status': ('burn', 0.2)},
	'fire blast':    {'target': 'opponent', 'amount': 2.8, 'cost': 30, 'element': 'fire',    'animation': 'fire_blast', 'status': ('burn', 0.3), 'accuracy': 85},
	# water and ice
	'water gun':     {'target': 'opponent', 'amount': 1.0, 'cost': 10, 'element': 'water',   'animation': 'water_gun', 'priority': 1},
	'geyser':        {'target': 'opponent', 'amount': 2.2, 'cost': 24, 'element': 'water',   'animation': 'geyser', 'accuracy': 90},
	'mud bomb':      {'target': 'opponent', 'amount': 1.4, 'cost': 16, 'element': 'water',   'animation': 'mud_bomb', 'stat': ('speed', -1), 'stat_chance': 0.5},
	'ink spray':     {'target': 'opponent', 'amount': 1.2, 'cost': 14, 'element': 'water',   'animation': 'ink_spray', 'stat': ('attack', -1), 'stat_chance': 0.5},
	'ice burst':     {'target': 'opponent', 'amount': 1.8, 'cost': 20, 'element': 'ice',     'animation': 'ice_burst', 'status': ('freeze', 0.2)},
	'diamond dust':  {'target': 'opponent', 'amount': 1.3, 'cost': 14, 'element': 'ice',     'animation': 'diamond_dust', 'stat': ('defense', -1), 'stat_chance': 0.3},
	# plant, poison and bug
	'wood hammer':   {'target': 'opponent', 'amount': 2.4, 'cost': 26, 'element': 'plant',   'animation': 'wood_hammer', 'accuracy': 90},
	'root bind':     {'target': 'opponent', 'amount': 1.0, 'cost': 12, 'element': 'plant',   'animation': 'root_bind', 'stat': ('speed', -1), 'stat_chance': 0.7},
	'seed cannon':   {'target': 'opponent', 'amount': 1.6, 'cost': 18, 'element': 'plant',   'animation': 'seed_cannon'},
	'toxic bomb':    {'target': 'opponent', 'amount': 2.0, 'cost': 22, 'element': 'poison',  'animation': 'toxic_bomb', 'status': ('poison', 0.4)},
	'leech bite':    {'target': 'opponent', 'amount': 1.3, 'cost': 14, 'element': 'bug',     'animation': 'leech_bite', 'stat': ('defense', -1), 'stat_chance': 0.3},
	# rock
	'rock slide':    {'target': 'opponent', 'amount': 1.8, 'cost': 20, 'element': 'rock',    'animation': 'rock_slide', 'stat': ('speed', -1), 'stat_chance': 0.3},
	'rock smash':    {'target': 'opponent', 'amount': 1.3, 'cost': 14, 'element': 'rock',    'animation': 'rock_smash', 'stat': ('defense', -1), 'stat_chance': 0.5},
	'sandstorm':     {'target': 'opponent', 'amount': 1.0, 'cost': 12, 'element': 'rock',    'animation': 'sandstorm', 'status': ('confused', 0.3)},
	'iron wall':     {'target': 'player',   'amount': 0,   'cost': 18, 'element': 'rock',    'animation': 'iron_wall', 'kind': 'status', 'stat': ('defense', 2)},
	# flying (lightning)
	'zap peck':      {'target': 'opponent', 'amount': 1.2, 'cost': 12, 'element': 'flying',  'animation': 'zap_peck', 'priority': 1},
	'thunder wave':  {'target': 'opponent', 'amount': 0,   'cost': 12, 'element': 'flying',  'animation': 'thunder_wave', 'kind': 'status', 'stat': ('speed', -2), 'accuracy': 90},
	# psychic
	'psy nova':      {'target': 'opponent', 'amount': 2.6, 'cost': 30, 'element': 'psychic', 'animation': 'psy_nova', 'accuracy': 85},
	'star burst':    {'target': 'opponent', 'amount': 1.6, 'cost': 18, 'element': 'psychic', 'animation': 'star_burst', 'stat': ('defense', -1), 'stat_chance': 0.3},
	'slow pulse':    {'target': 'opponent', 'amount': 0,   'cost': 12, 'element': 'psychic', 'animation': 'slow_pulse', 'kind': 'status', 'stat': ('speed', -2)},
	'doom pulse':    {'target': 'opponent', 'amount': 3.0, 'cost': 32, 'element': 'psychic', 'animation': 'doom_pulse', 'charge': True},
	'calm mind':     {'target': 'player',   'amount': 0,   'cost': 16, 'element': 'psychic', 'animation': 'calm_mind', 'kind': 'status', 'stat': ('defense', 2)},
	'recover':       {'target': 'player',   'amount': 0,   'cost': 26, 'element': 'psychic', 'animation': 'heal_sparkle', 'kind': 'heal', 'heal': 0.5},
	'glitch wave':   {'target': 'opponent', 'amount': 1.5, 'cost': 16, 'element': 'psychic', 'animation': 'glitch', 'status': ('confused', 0.3)},
}

# ITEM_DATA: which stat an item restores and what fraction of the maximum it gives back
ITEM_DATA = {
	'potion': {'stat': 'health', 'max_stat': 'max_health', 'ratio': 0.5},
	'ether':  {'stat': 'energy', 'max_stat': 'max_energy', 'ratio': 0.5},
	# Iteration 21: items that cure a status effect (only useful in battle; statuses end with the battle)
	'burn_heal':  {'cures': ('burn',)},
	'thaw_spray': {'cures': ('freeze',)},
	'antidote':   {'cures': ('poison',)},
	'wake_bell':  {'cures': ('sleep',)},
	'full_cure':  {'cures': ('burn', 'freeze', 'poison', 'sleep', 'confused')},
	# Iteration 25
	'max_ether':  {'stat': 'energy', 'max_stat': 'max_energy', 'ratio': 1.0},
	'party_heal': {'field': 'party_heal'},    # heals every party monster, used from the bag
	# (Iteration 31: Repel and Escape Rope were removed)
}

# Iteration 25: key items are kept for ever and are never used up.
# Iteration 31: fishing, digging, hidden items and crafting were removed, so the only key item left is the
# Shiny Charm (an achievement reward) and there are no materials any more.
KEY_ITEMS = ('shiny_charm',)
MATERIALS = {}   # name -> selling price (none since Iteration 31)
REMOVED_ITEMS = ('repel', 'escape_rope', 'fishing_rod', 'shovel', 'swift_cap', 'snow_boots', 'pearl', 'fossil', 'crystal', 'scrap', 'herb', 'egg')

# items every new playthrough starts with
STARTING_INVENTORY = {'potion': 5, 'ether': 3, 'capture_orb': 5}

# STARTER_MONSTERS: the three monsters the player can choose from on a new game (Iteration 13),
# shown in this order in the starter carousel. STARTER_LEVEL is the level they start at.
STARTER_MONSTERS = ('Plumette', 'Sparchu', 'Finsta')
STARTER_LEVEL = 5

# WILD_ENCOUNTERS: which monsters appear in each zone's grass and at what level (Iteration 13).
# The grass (forest) zone has first-stage monsters, the sand zone second-stage monsters and the
# ice zone the strongest, final-stage monsters. pick = the most wild monsters that appear at once.
WILD_ENCOUNTERS = {
	# Iteration 23: the new monsters live in the wild too
	'forest': {'monsters': ('Plumette', 'Sparchu', 'Finsta', 'Larvea', 'Jacana', 'Pouch'), 'levels': (3, 7), 'pick': 1},   # Iteration 15: one at a time near the start
	'sand':   {'monsters': ('Ivieron', 'Cindrill', 'Gulfin', 'Cleaf', 'Atrox', 'Pouch'), 'levels': (7, 11), 'pick': 1},   # Iteration 18: was 12-18, too strong next to the beach trainers
	'ice':    {'monsters': ('Pluma', 'Charmadillo', 'Finiette', 'Friolera', 'Draem'), 'levels': (30, 38), 'pick': 2},
}

# HELD_ITEM_DATA: items a monster can hold (one per monster). effect says what the item changes and
# multiplier says by how much, e.g. 1.25 = 25% more. Used by Monster.held_multiplier.
HELD_ITEM_DATA = {
	'power_band':   {'effect': 'damage',      'multiplier': 1.25},   # attacks do 25% more damage
	'vital_charm':  {'effect': 'max_health',  'multiplier': 1.2},    # 20% more maximum health
	'focus_ring':   {'effect': 'energy_cost', 'multiplier': 0.75},   # attacks cost 25% less energy
	'wise_feather': {'effect': 'xp',          'multiplier': 1.5},    # 50% more experience
	# Iteration 25
	'swift_scarf':  {'effect': 'speed',       'multiplier': 1.2},    # takes turns 20% more often
	'guard_shell':  {'effect': 'defense',     'multiplier': 1.25},   # 25% more defence
	'lucky_coin':   {'effect': 'coins',       'multiplier': 1.5},    # 50% more coins from trainers
}

# BADGE_DATA: the main trainers that give a badge when beaten, in the order the game expects you to
# beat them (used by the map to suggest who to fight next). reward = held item and extra items given.
BADGE_DATA = {
	'o1': {'badge': 'Rookie',  'reward': {'held': 'power_band',   'items': {'potion': 1}}},   # first trainer next to the house
	'o3': {'badge': 'Shell',   'reward': {'held': 'wise_feather', 'items': {'potion': 1}}},   # beach girl who looks around
	'o2': {'badge': 'Sunny',   'reward': {'held': 'vital_charm',  'items': {'ether': 1}}},    # blonde girl on the beach
	'o4': {'badge': 'Meadow',  'reward': {'held': 'focus_ring',   'items': {'potion': 1}}},
	'o5': {'badge': 'Grove',   'reward': {'held': 'power_band',   'items': {'ether': 1}}},
	'px': {'badge': 'Leaf',    'reward': {'held': 'focus_ring',   'items': {'potion': 2, 'ether': 1}}},   # plant gym leader
	'o6': {'badge': 'Frost',   'reward': {'held': 'vital_charm',  'items': {'potion': 1}}},
	'fx': {'badge': 'Flame',   'reward': {'held': 'power_band',   'items': {'potion': 2, 'ether': 1}}},   # fire gym leader
	'o7': {'badge': 'Glacier', 'reward': {'held': 'wise_feather', 'items': {'ether': 1}}},    # small boy in the snow
	'wx': {'badge': 'Tide',    'reward': {'held': 'vital_charm',  'items': {'potion': 2, 'ether': 2}}},   # water gym leader
}

# Iteration 14
# CAPTURE_ORB_DATA: orbs used to catch wild monsters. rate multiplies the chance of a catch:
# chance = rate * (1.1 - health / max health), so a weaker monster is easier to catch.
CAPTURE_ORB_DATA = {
	'capture_orb': {'rate': 1.0},
	'great_orb':   {'rate': 1.6},
	'prime_orb':   {'rate': 2.5},
}

# QUEST_DATA (Iteration 16): side quests and achievements. kind says what is counted (worked out by
# Game.quest_progress), target is the amount needed and reward is given when the player claims it.
# Completing the monster index ('caught' all species) is the biggest reward.
QUEST_DATA = {
	'first_catch':  {'kind': 'catches',  'target': 1,  'reward': {'items': {'capture_orb': 3}}},
	'catch_5':      {'kind': 'caught',   'target': 5,  'reward': {'items': {'great_orb': 3}}},
	'catch_10':     {'kind': 'caught',   'target': 10, 'reward': {'coins': 500}},
	'complete_dex': {'kind': 'caught',   'target': 16, 'reward': {'coins': 2000, 'items': {'prime_orb': 3}}},   # Iteration 27: the 16 original monsters
	'see_all':      {'kind': 'seen',     'target': 16, 'reward': {'coins': 300}},
	'first_badge':  {'kind': 'badges',   'target': 1,  'reward': {'items': {'potion': 3}}},
	'badges_5':     {'kind': 'badges',   'target': 5,  'reward': {'items': {'focus_ring': 1}}},
	'all_badges':   {'kind': 'badges',   'target': 10, 'reward': {'coins': 3000}},
	'first_evolve': {'kind': 'evolved',  'target': 1,  'reward': {'items': {'wise_feather': 1}}},
	'level_20':     {'kind': 'level',    'target': 20, 'reward': {'items': {'vital_charm': 1}}},
	'full_party':   {'kind': 'party',    'target': 6,  'reward': {'items': {'potion': 5, 'ether': 5}}},
	'shiny':        {'kind': 'shiny',    'target': 1,  'reward': {'items': {'prime_orb': 1}}},
	'savings':      {'kind': 'coins',    'target': 1000, 'reward': {'items': {'power_band': 1}}},
}

# SHOP_PRICES: what the nurse sells and how many coins each costs. Held items cost the most.
SHOP_PRICES = {
	'potion': 30, 'ether': 40,
	'capture_orb': 50, 'great_orb': 150, 'prime_orb': 400,
	'power_band': 600, 'vital_charm': 600, 'focus_ring': 600, 'wise_feather': 800,
	'burn_heal': 60, 'thaw_spray': 60, 'antidote': 60, 'wake_bell': 60, 'full_cure': 200,   # Iteration 21
	'illuminator': 3000,   # Iteration 18: the most expensive item - makes a monster shiny
	# Iteration 25
	'max_ether': 120, 'party_heal': 250, 'swift_scarf': 700, 'guard_shell': 700, 'lucky_coin': 900,
}

# Iteration 25: the shop's stock grows with the badges you have. Anything not listed is always sold.
SHOP_UNLOCK = {
	'great_orb': 2, 'burn_heal': 1, 'thaw_spray': 1, 'antidote': 1, 'wake_bell': 1,
	'max_ether': 3, 'full_cure': 3, 'party_heal': 4, 'prime_orb': 5,
	'power_band': 3, 'vital_charm': 3, 'focus_ring': 4, 'wise_feather': 4, 'swift_scarf': 5, 'guard_shell': 5, 'lucky_coin': 6, 'illuminator': 8,
}
DAILY_DISCOUNT = 0.3   # one item a day is 30% cheaper

# Iteration 25: monsters that only come out at night (added to that zone's grass from 20:00 to 6:00)
NIGHT_ENCOUNTERS = {'forest': ('Draem', 'Atrox'), 'sand': ('Draem', 'Friolera'), 'ice': ('Draem',)}
NIGHT_ONLY = ()   # monsters never seen in daylight (none since Iteration 27)

# Iteration 18: items that do something special when used on a monster (not healing or held)
SPECIAL_ITEMS = ('illuminator',)

# Iteration 27: only the 16 original monsters are in the game. Monsters added in Iterations 23-26 that are
# still in a save become an original monster of the same type, so old saves keep loading.
RENAMED = {'Venofrog': 'Atrox', 'Toxitoad': 'Atrox', 'Gloop': 'Atrox', 'Toxwraith': 'Atrox',
           'Mothlit': 'Cleaf', 'Gremlit': 'Cleaf', 'Chirpi': 'Jacana', 'Galeon': 'Jacana', 'Puffghost': 'Jacana', 'Galewraith': 'Jacana',
           'Mindle': 'Draem', 'Cerebloom': 'Draem', 'Hexie': 'Draem', 'Hexmage': 'Draem', 'Codeus': 'Draem',
           'Frostbun': 'Friolera', 'Glacihare': 'Friolera', 'Frostie': 'Friolera', 'Glacigolem': 'Friolera'}

def current_name(name):
	return RENAMED.get(name, name)

# Iteration 33: the new moves are shared out, so most moves can be learnt by more than one monster.
# (level -> move; added to each monster's own list)
_PLANT = {5: 'root bind', 14: 'seed cannon', 24: 'wood hammer'}
_FIRE = {5: 'flame wheel', 9: 'spark shower', 13: 'blue flame', 20: 'firework', 23: 'flame burst', 34: 'fire blast'}
_WATER = {5: 'water gun', 10: 'mud bomb', 16: 'ink spray', 22: 'geyser'}
EXTRA_MOVES = {
	'Plumette': _PLANT, 'Ivieron': {**_PLANT, 35: 'toxic bomb'}, 'Pluma': {**_PLANT, 35: 'toxic bomb', 38: 'iron wall'},
	'Sparchu': _FIRE, 'Cindrill': {**_FIRE, 38: 'heat wave'},
	'Charmadillo': {**_FIRE, 24: 'rock smash', 28: 'rock slide', 36: 'sandstorm', 38: 'heat wave', 44: 'iron wall'},
	'Finsta': _WATER, 'Gulfin': {**_WATER, 30: 'body slam'}, 'Finiette': {**_WATER, 30: 'body slam', 36: 'ice burst', 40: 'diamond dust'},
	'Atrox': {2: 'smokescreen', 7: 'leech bite', 16: 'toxic bomb', 18: 'taunt', 24: 'sandstorm'},
	'Pouch': {2: 'coin toss', 4: 'charm', 7: 'war cry', 9: 'riddle', 10: 'body slam', 11: 'sing', 16: 'scary face',
	          22: 'agility', 24: 'focus energy', 28: 'hyper blast', 32: 'taunt', 35: 'smokescreen'},
	'Draem': {2: 'slow pulse', 6: 'star burst', 10: 'glitch wave', 11: 'riddle', 14: 'calm mind', 18: 'recover', 25: 'psy nova', 30: 'doom pulse'},
	'Larvea': {2: 'leech bite'},
	'Cleaf': {2: 'leech bite', 10: 'smokescreen', 14: 'root bind', 20: 'seed cannon', 24: 'wood hammer', 28: 'toxic bomb'},
	'Jacana': {2: 'zap peck', 10: 'thunder wave', 12: 'agility', 18: 'scary face', 22: 'body slam', 30: 'hyper blast'},
	'Friolera': {2: 'diamond dust', 10: 'charm', 14: 'sing', 20: 'ice burst', 26: 'calm mind', 30: 'geyser'},
}
for _name, _moves in EXTRA_MOVES.items():
	_taken = set(MONSTER_DATA[_name]['abilities'])
	_clash = _taken & set(_moves)
	assert not _clash, f'{_name} already learns a move at level {_clash}'
	MONSTER_DATA[_name]['abilities'] = dict(sorted({**MONSTER_DATA[_name]['abilities'], **_moves}.items()))

# ---------- Iteration 35: the move list after playtesting in training mode ----------
# Removed: Spark, Fire, Flame Wheel, Ember Dash, Firework, Root Bind, Seed Shot, Water Gun, Splash and Soak.
# Renamed: Grassy Heal is now Bramble Cage (an attack - its animation looks like a cage), Aqua Jet is now the ice
# move Frost Jet, Ink Spray is now the poison move Toxic Splash. Leaf Storm heals instead. Bubble uses the bubble
# animation (from Soak). Venom Burst and Toxic swapped animations. New types: dark, ghost and fairy.
REMOVED_MOVES = {   # an old save's moves are changed to these
	'spark': 'spark shower', 'fire': 'flame burst', 'flame wheel': 'spark shower', 'ember dash': 'blue flame',
	'firework': 'flame burst', 'root bind': 'bramble cage', 'seed shot': 'vine whip', 'water gun': 'bubble',
	'splash': 'bubble', 'soak': 'bubble', 'grassy heal': 'bramble cage', 'aqua jet': 'frost jet', 'ink spray': 'toxic splash',
}
def current_move(move):
	return REMOVED_MOVES.get(move, move)

ATTACK_DATA['bramble cage'] = {'target': 'opponent', 'amount': 1.4, 'cost': 16, 'element': 'plant', 'animation': 'grass_grow', 'stat': ('speed', -1), 'stat_chance': 1.0}
ATTACK_DATA['frost jet'] = {**ATTACK_DATA['aqua jet'], 'element': 'ice'}
ATTACK_DATA['toxic splash'] = {'target': 'opponent', 'amount': 1.2, 'cost': 14, 'element': 'poison', 'animation': 'ink_spray', 'status': ('poison', 0.3)}
for _move in REMOVED_MOVES:
	ATTACK_DATA.pop(_move, None)

ATTACK_DATA['leaf storm'] = {'target': 'player', 'amount': 0, 'cost': 26, 'element': 'plant', 'animation': 'green', 'kind': 'heal', 'heal': 0.45}
ATTACK_DATA['bubble'].update({'animation': 'soak', 'sound': 'splash'})
ATTACK_DATA['sleep spores'].update({'element': 'bug', 'scale': 1.6})
ATTACK_DATA['solar beam'].update({'animation': 'solar_beam'})
ATTACK_DATA['venom burst'].update({'animation': 'toxic', 'scale': 1.7})
ATTACK_DATA['toxic'].update({'animation': 'venom'})
ATTACK_DATA['doom pulse'].update({'element': 'normal'})
ATTACK_DATA['dark pulse'] = {'target': 'opponent', 'amount': 3.2, 'cost': 34, 'element': 'dark', 'animation': 'dark_pulse', 'accuracy': 90, 'scale': 1.7,
                             'stat': ('attack', -1), 'stat_chance': 0.3}   # a finishing move
for _move, _element in (('taunt', 'dark'), ('glare', 'dark'), ('nightmare', 'ghost'), ('smokescreen', 'ghost'), ('scary face', 'ghost'),
                        ('star burst', 'fairy'), ('charm', 'fairy'), ('sing', 'fairy')):
	ATTACK_DATA[_move]['element'] = _element

_PLANT = {0: 'scratch', 3: 'vine whip', 7: 'petal spit', 10: 'bramble cage', 14: 'seed cannon', 20: 'leaf storm', 24: 'wood hammer', 28: 'solar beam'}
_FIRE = {0: 'scratch', 3: 'spark shower', 7: 'burn', 10: 'power up', 13: 'blue flame', 15: 'fire pillar', 18: 'flame burst', 26: 'explosion', 34: 'fire blast'}
_WATER = {0: 'scratch', 3: 'bubble', 7: 'frost jet', 9: 'guard up', 10: 'mud bomb', 14: 'heal', 18: 'geyser', 25: 'tidal wave'}
LEARNSETS_35 = {
	'Plumette': _PLANT,
	'Ivieron': {**_PLANT, 16: 'toxic splash', 35: 'toxic bomb'},
	'Pluma': {**_PLANT, 16: 'toxic splash', 35: 'toxic bomb', 38: 'iron wall'},
	'Sparchu': _FIRE,
	'Cindrill': {**_FIRE, 38: 'heat wave'},
	'Charmadillo': {**_FIRE, 22: 'rock throw', 24: 'rock smash', 28: 'rock slide', 30: 'inferno', 36: 'sandstorm', 38: 'heat wave', 40: 'annihilate', 44: 'iron wall'},
	'Finsta': _WATER,
	'Gulfin': {**_WATER, 30: 'body slam', 32: 'ice'},
	'Finiette': {**_WATER, 30: 'body slam', 32: 'ice', 36: 'ice burst', 40: 'diamond dust'},
	'Atrox': {0: 'poison sting', 2: 'smokescreen', 4: 'acid flick', 6: 'acid spray', 7: 'leech bite', 9: 'toxic', 11: 'glare', 13: 'toxic splash',
	          14: 'bug bite', 16: 'toxic bomb', 18: 'taunt', 20: 'venom burst', 24: 'sandstorm'},
	'Draem': {0: 'mind pulse', 2: 'slow pulse', 4: 'blink', 6: 'star burst', 7: 'confuse ray', 9: 'hypnosis', 10: 'glitch wave', 11: 'riddle',
	          14: 'calm mind', 18: 'recover', 20: 'nightmare', 22: 'future sight', 25: 'psy nova', 30: 'doom pulse', 34: 'dark pulse'},
	'Larvea': {0: 'bug bite', 2: 'leech bite', 3: 'silk trap', 4: 'sleep spores', 5: 'acid spray'},
	'Cleaf': {0: 'bug bite', 2: 'leech bite', 3: 'silk trap', 5: 'acid spray', 6: 'swarm rush', 8: 'sleep spores', 9: 'acid pool', 10: 'smokescreen',
	          12: 'vine whip', 14: 'bramble cage', 18: 'megahorn', 20: 'seed cannon', 24: 'wood hammer', 28: 'toxic bomb'},
}
for _name, _moves in LEARNSETS_35.items():
	MONSTER_DATA[_name]['abilities'] = dict(sorted(_moves.items()))
for _name, _data in MONSTER_DATA.items():   # every other monster just loses the removed moves
	_data['abilities'] = {level: current_move(move) for level, move in _data['abilities'].items() if current_move(move) in ATTACK_DATA}
MONSTER_DATA['Jacana']['abilities'].pop(14, None)   # (Spark became Spark Shower, a fire move - not for Jacana)
MONSTER_DATA['Friolera']['abilities'][15] = 'frost jet'

# every main type keeps one quick move that goes first (their old quick moves were removed above)
ATTACK_DATA['spark shower'].update({'priority': 1, 'amount': 1.1})
ATTACK_DATA['vine whip'].update({'priority': 1, 'amount': 1.2})
ATTACK_DATA['bubble'].update({'priority': 1, 'amount': 1.2})
