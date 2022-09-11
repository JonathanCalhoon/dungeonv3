from generators import dungeon
from code import game, map, terminal, util
from classes import player
from save_game import menu, save, save_util
from settings import settings
import random
import config
import character_picker




###################
#  INIT SETTINGS  #
###################

settings = settings.Settings()

# delete all saves

if not config.SAVE:
	save.delete_all_saves()


class LoginManager():
	def __init__(self):
		"""Initate the Login Manager"""
		pass # litterally does nothing :(

	def example():
		"""Example Menu (no save)"""

		return menu.show_example()
		

	def login(self):
		"""Handle User Login and Player/Map Restore"""

		if menu.show_menu():
			terminal.clear()
			saves = save.get_saves()

			print("SELECT SAVE: ")

			valids = []
			
			for i in saves:
				index = str(saves.index(i))
				print(f"[{index}] {i['name']} | {i['date']}")
				valids.append(index)

			i = int(util.get_input("-> ", valids))

			game_save = saves[i]

			game_data = save.get_game_data(game_save)

			g = game.Game(
				settings,
				dungeon=(game_data[1], game_data[2]),
				player=game_data[0],
				posx=game_data[3],
				posy=game_data[4],
				filename=game_data[5],
			)

			return g
			

		else:
			terminal.clear()
			print("Creating New Game")
			print("\n\n")

			name = input("Save Name: ")

			filename = save.add_save(name)

			p = player.Player()

			p.character = character_picker.pick_character()
			p.give_boosts()

			mygame = game.Game(
				settings,
				dungeon = dungeon.build_dungeon(p),
				player=p,
				filename=filename,
			)

			return mygame
					

			

			



				
				

		