import json
from classes import weapon, armor, player
import os
from datetime import date
from save_game import save_util
from generators import dungeon
import glob, shutil
from generators import monsters





def delete_all_saves():
	"""Deletes all Saves"""

	files = glob.glob('saves/*')
	for f in files:
		if os.path.isfile(f):
			os.system("rm " + f)
		else:
			shutil.rmtree(f)

	with open('saves/saves.txt', 'x') as file:
		pass
	with open('saves/saves.txt', 'w') as file:
		file.write(json.dumps({"saves":[],"count":1}))

	

def get_game_data(save):
	"""Converts 'nested' JSON to 'nested' Game Data and Player Object"""

	with open(f"saves/save_{save['val']}/save.txt", "r") as file:
		save_data = json.loads(file.read())

	p = player.Player()
	p.restore(save_data['player'])

	game_map = save_util.map_from_file(f"saves/save_{save['val']}/map.txt")

	enemies = monsters.get_enemies_from_list(save_data['enemies'])

	posx = save_data['posx']
	posy = save_data['posy']

	return [p, game_map, enemies, posx, posy, save['val']]




def save_player_data(player, enemies, posx, posy, save_num):
	"""Writes Player Data to File"""

	JSON = {
		'player' : save_util.class_to_json(player),
		'posx' : posx,
		'posy' : posy,
		'enemies' : monsters.enemies_to_strings(enemies),
	}

	with open(f"saves/save_{str(save_num)}/save.txt", 'w') as file:
		file.write(json.dumps(JSON))


def save_map_data(save_num, level, map):
	"""Save the map to file"""
	with open(f"saves/save_{str(save_num)}/map.txt", 'w') as file:
		data = save_util.map_to_string(map)
		file.write(data)




def get_saves():
	"""Get the list of saves"""
	with open('saves/saves.txt', 'r') as file:
		data = json.loads(file.read())

	return data['saves']


def add_save(name):
	global save
	"""Add a save to the list of saves"""

	with open('saves/saves.txt', 'r') as file:
		data = json.loads(file.read())

	val = data['count']

	os.mkdir('saves/save_'+str(val))

	with open('saves/save_'+str(val)+'/save.txt', 'x') as file:
		pass

	with open('saves/save_'+str(val)+"/map.txt", 'x') as file:
		pass


	data['count'] += 1

	save = {
		'name' : name,
		'date' : str(date.today()),
		'val' : val
	}

	data['saves'].append(save)

	with open('saves/saves.txt', 'w') as file:
		file.write(json.dumps(data))

	return val



# New Saves Format: 

"""
/saves
| -- saves.txt
| -- /save_<id>
|    | -- save.txt
|    | -- map.txt
"""


					

		

		
		