from code import terminal, util, screen
from getkey import getkey
from classes import player
from save_game import save
from settings import settings
from leaderboard import leaderboard
import time


screen = screen.Screen()
settings = settings.Settings()
leaderboard = leaderboard.Leaderboard()


with open("save_game/menu.txt", "r") as file:
	data = file.read()

mymenu = data.split("\n")


def show_menu():
	"""Display The Menu"""
	terminal.clear()

	choice = screen.get_input(
		question=mymenu,
		raw_prompts=[
			("Restore Save", 1),
			("Start New", 2),
			("Tutorial", 3),
			("Leaderboard", 4),
			("Exit", 5)
		]
	)

	if choice == 1:
		return True
	elif choice == 2:
		return False
	elif choice == 3:
		return tutorial()
	elif choice == 4:
		leaderboard.display()
		return show_menu()
	elif choice == 5:
		exit()


def tutorial():
	"""Display Tutorial and call Menu Again"""

	with open('assets/tutorial.txt', 'r') as file:
		parts = file.read().split('\nPART\n')

	for part in parts:
		terminal.clear()
		result = screen.display_out(part, auto_print=False)
		for line in result:
			print(line)
			time.sleep(.05)
		util.cont()

	return show_menu()