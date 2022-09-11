import json
from code import screen, terminal, util
import config
from better_profanity import profanity
import random

# Note: Due to previous knowledge of replit users, I should
# probably refuse any usernames that aren't going to "cut it"


# These are extremely toxic words that cannot be allowed!
profanity.add_censor_words(["toxic", "amongus", "sus", "imposter", "fortnite", "clashroyale", "clash", "royale", "susposter", "redsus", "red"])



class Leaderboard():
	def __init__(self):
		self.screen = screen.Screen(colors=["\033[0m","\033[1m","\033[4m"])
		self.database_type = config.DB

		self.load_data()


	def get_username(self):
		"""Get a username from the player and check for anything illegal"""
		while True:
			username = input("Username (For Leaderboard):\n>>> ")
			if profanity.contains_profanity(username):
				print("Your username contains profanity and will not be accepted!")
				util.cont()
			elif self.username_taken(username):
				print("This username has already been taken!")
				util.cont()
			elif len(username)>15:
				print("This username is too long!")
				util.cont()
			else:
				return username


	def username_taken(self, username):
		"""Check if a username has already been taken"""
		for record in self.leader_data:
			if record['username'] == username:
				return True
		return False


	def load_data(self):
		"""Get the leaderboard data"""
		if self.database_type == "txt":
			with open('leaderboard/leaderboard.txt', 'r') as file:
				self.leader_data = sorted(json.loads(file.read()), key=lambda sortby: sortby["gold"])
				self.leader_data.reverse()
				if len(self.leader_data) > 20:
					self.leader_data = self.leader_data[:20]


	def display(self):
		"""Display the leaderboard"""

		table = [["\033[1m\033[4m#", "Username", "Gold", "Depth", "Level\033[0m"]]

		for user in self.leader_data:
			table.append([self.leader_data.index(user)+1, user['username'], user['gold'], user['depth'], user['level']])


		self.screen.display_table(table=table) # classic programmer technique #213: Call a function that doesn't exist and worry about it later
		util.cnt()


	def add_record(self, player):
		"""Add a record to the leaderboard"""

		if len(self.leader_data) < 20 or player.gold > self.leader_data[-1]['gold']:

			username = self.get_username()

			self.leader_data.append({
					"username":username,
					"gold":player.gold,
					"depth":player.dungeon_level,
					"level":player.level,
				})

			with open("leaderboard/leaderboard.txt", "w") as file:
				file.write(json.dumps(self.leader_data))

			self.leader_data = sorted(self.leader_data, key=lambda sortby: sortby["gold"])
			self.leader_data.reverse()

		else:
			# Trash Noob
			return


			


