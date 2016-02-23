"""
This is just a bunch of magic numbers used by the ygopro database.
Nobody other than ygopro.py should ever need to import this.
Got a lot of help from https://www.ygopro.co/Forum/tabid/95/g/posts/t/120/Adding-cards-to-YGOPro--Tutorial----Scripting-video-Added.
"""

# This whole page is a mess. I'll clean it up if it ends up biting me in the butt.
attributes = {
		'N/A'   : 0,
		'EARTH' : 1,
		'WATER' : 2,
		'FIRE' :  4,
		'WIND' :  8,
		'LIGHT' : 16,
		'DARK' :  32,
		'DIVINE' : 64
	}
types = {
		'N/A'   : 0,
		'Warrior' :       1,
		'Spellcaster' :   2,
		'Fairy' :         4,
		'Fiend' :         8,
		'Zombie' :        16,
		'Machine' :       32,
		'Aqua' :          64,
		'Pyro' :          128,
		'Rock' :          256,
		'Winged-Beast':   512,
		'Plant' :         1024,
		'Insect' :        2048,
		'Thunder' :       4096,
		'Dragon' :        8192,
		'Beast' :         16384,
		'Beast-Warrior' : 32768,
		'Dinosaur' :      65536,
		'Fish' :          131072,
		'Sea-Serpent' :   262144,
		'Reptile' :       524288,
		'Psychic' :       1048576,
		'Divine-Beast' :  2097152,
		'Creator-God' :   4194304,
		'Wyrm' :          8388608,
	}
availability = {
		'OCG' : 1,
		'TCG' : 2,
		'Any' : 3,
		'Anime' : 4,
	}
category = {
		'Normal-Spell':                 2,
		'Normal-Trap':                  4,
		'Normal-Monster':               17,
		'Effect-Monster':               33,
		'Fusion-Monster':               65,
		'Fusion-Effect-Monster':        97,
		'Ritual-Monster':               129,
		'Ritual-Spell':                 130,
		'Ritual-Effect-Monster':        161,
		'Spirit-Effect-Monster':        545,
		'Union-Effect-Monster':         1057,
		'Gemini-Monster':               2081,
		'Tuner-Monster':                4113,
		'Tuner-Effect-Monster':         4129,
		'Synchro-Monster':              8193,
		'Synchro-Effect-Monster':       8225,
		'Synchro-Tuner-Effect-Monster': 12321,
		'Anime-Card' :                  16384,
		'Token':                        16401,
		'Quick-Play-Spell':             65538,
		'Continuous-Spell':             131074,
		'Continuous-Trap':              131076,
		'Equip-Spell':                  262146,
		'Field-Spell':                  524290,
		'Counter-Trap':                 1048580,
		'Flip-Effect-Monster':          2097185,
		'Flip-Tuner-Effect-Monster':    2101281, # Shaddoll Falco is the only one
		'Toon-Effect-Monster':          4194337,
		'Xyz-Monster':                  8388609,
		'Xyz-Effect-Monster':           8388641,
		'Normal-Pendulum-Monster' :            16777233,
		'Pendulum-Effect-Monster' :     16777249,
		'Pendulum-Tuner-Effect-Monster':16781345,
		'Xyz-Pendulum-Effect-Monster' : 25165857,
	}
MAGIC_NUMBERS = {
	'attribute' : attributes,
	'type' : types,
	'banlist' : availability,
	'category' : category
}

# this is not really useful anymore, but I'm not going to delete it.
MONSTER = set([17, 33, 65, 97, 129, 161, 545, 1057, 2081, 4113, 4129, 8193, 8225, 12321, 16401, 2097185, 4194337, 8388609, 8388641, 16777233, 16777249])
SPELL = set([2, 130, 65538, 131074, 262146, 524290])
TRAP = set([4, 131076, 1048580])
PENDULUM = set([16777233, 16777249])
SYNCHRO = set([8193,8225,12321])
XYZ = set([8388609, 8388641])
TUNER = set([4113, 4129, 12321])
NON_EFFECT = set([8388609, 16777233, 8193, 4113, 17])
RITUAL = set([129, 161])

def invert(d):
	return dict((y, x) for (x, y) in d.items())
MAGIC_NUMBERS_I = dict((key, invert(value)) for key, value in MAGIC_NUMBERS.items())

class EnumError(RuntimeError): pass

def get_string(section, value):
	'''given a database number, get the string that represents it'''
	enum_sect = MAGIC_NUMBERS_I.get(section, None)
	if enum_sect:
		if value in enum_sect:
			return enum_sect[value]
		else:
			raise EnumError('There is no {0} with database id of {1}'.format(section, value))
	else:
		raise EnumError('{0} is not a valid kind of enum. Options are {1}'.format(section, ', '.join(MAGIC_NUMBERS_I.keys())))
			
def get_db_value(section, value):
	'''given a an enum name, get the database number of it'''
	enum_sect = MAGIC_NUMBERS.get(section, None)
	if enum_sect:
		if value in enum_sect:
			return enum_sect[value]
		else:
			raise EnumError('There is no {0} with database id of {1}'.format(section, value))
	else:
		raise EnumError('{0} is not a valid kind of enum. Options are {1}'.format(section, ', '.join(MAGIC_NUMBERS.keys())))