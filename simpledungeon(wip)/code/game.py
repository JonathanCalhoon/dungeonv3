from code import terminal, map, randomness, util, screen
from battle import battle
from getkey import getkey, keys
import random, time, sys
from classes import weapon, armor
from generators import monsters, dungeon
from save_game import save, save_util
from leaderboard import leaderboard


class Game():
	def __init__(self, settings, dungeon, player, posx=False, posy=False, filename=None):
		"""Initiate the Game"""

		self.screen = screen.Screen(settings.colors)

		self.leaderboard = leaderboard.Leaderboard()

		self.filename = filename

		self.settings = settings
		
		self.dungeon = dungeon[0]

		self.enemies = dungeon[1]

		self.player = player

		if not posx and not posy:
			self.y, self.x = map.getSpawn(self.dungeon)
		else:
			self.y = posy
			self.x = posx


	def gen_dungeon(self):
		"""Generate a dungeon and move to it"""

		dungeon_vals = dungeon.build_dungeon(self.player)

		self.player.dungeon_level += 1
		self.player.xp += 3

		self.dungeon = dungeon_vals[0]
		self.enemies = dungeon_vals[1]
				
		self.y, self.x = map.getSpawn(self.dungeon)

		self.in_dungeon = True

		map.animate_entry(self.dungeon, self.x, self.y, self.settings, [self.player.get_stats()])

	def play(self):
		"""The main Game Loop"""
		play_count = 0

		map.animate_entry(self.dungeon, self.x, self.y, self.settings, [self.player.get_stats()])
		
		while True:
			# disabled count clear for now. Manual clear is still enabled
			self.player.level_up()
			play_count += 1
			if play_count == 20:
				#terminal.clear() # just to keep things from being messy
				play_count = 0
				save.save_player_data(self.player, self.enemies, self.x, self.y, self.filename)
				save.save_map_data(self.filename, self.player.dungeon_level, self.dungeon)

			stats = [self.player.get_stats()]
			
			map.display(self.settings, self.dungeon, self.x, self.y, stats)

			self.dungeon[self.y][self.x] = ' '

			key = getkey()

			x = self.x
			y = self.y
			
			if key == 'w' or key == keys.UP:
				y -= 1

			elif key == 's' or key == keys.DOWN:
				y += 1

			elif key == 'd' or key == keys.RIGHT:
				x += 1

			elif key == 'a' or key == keys.LEFT:
				x -= 1

			elif key == '1':
				self.player_stats()
			elif key == '2':
				self.player.shuffle_loadout()
			elif key == '3':
				save.save_player_data(self.player, self.enemies, self.x, self.y, self.filename)
				save.save_map_data(self.filename, self.player.dungeon_level, self.dungeon)
			elif key == '4':
				terminal.clear()
			elif key == '5':
				self.settings.setup()
			elif key == '6':
				self.win_game()
			elif key == '0':
				choice = self.screen.get_input(self.player, "Are you sure you want to exit?", raw_prompts=[("Yes", "yes"), ("No", "no")])
				if choice == 'yes':
					print("Saving...")
					save.save_player_data(self.player, self.enemies, self.x, self.y, self.filename)
					save.save_map_data(self.filename, self.player.dungeon_level, self.dungeon)
					exit()
				elif choice == 'no':
					terminal.clear()

			for enemy in self.enemies:
				enemy.move((self.y, self.x), self.dungeon, (self.y, self.x), self.player)

			if self.player.character == "skeleton":
				self.player.life = self.player.max_life

			#remove any dead
			for enemy in self.enemies:
				if enemy.dead:
					self.dungeon[enemy.y][enemy.x] = " "
					self.enemies.remove(enemy)


			item = self.dungeon[y][x]

			if item in ['#', '@', '.', '|', '-', '+']:
				valid = False
			else:
				valid = True

			if item == 't':
				self.open_treasure()

			if item == '@':
				self.gen_dungeon()

			if item in randomness.enemy_symbols:
				if item == "S" and self.player.character == "skeleton":
					self.screen.display_card(self.player, ["Your fellow Skelly waves hello"])
					util.cnt()
			
			if item == '*':
				self.collect_shard()

			if valid:
				self.y = y
				self.x = x


	def player_stats(self):
		"""Show the user inventory, armor, etc"""


		char = randomness.get_char(self.player)

		terminal.clear()

		card = ["", "", ""]

		
		char[2] += f"  SHARDS: {str(self.player.shards)}"
		char[4] += f"  LEVEL: {str(self.player.level)}"
		char[5] += f"  XP: {str(self.player.xp)}/{str(self.player.max_xp)}"

		for c in char:
			card.append(c)

		card.append("")

		card.append(self.player.weapon.stats())
		card.append(self.player.armor.stats())

		"""
		for item in sorted(self.player.inventory):
			exist = False
			for i in items:
				if item == i[0]:
					i[1] += 1
					exist = True
			if not exist:
				items.append([item, 1])

		for item in items:
			util.indent(f"{item[0]} x{str(item[1])}", 26)
		"""
		
		self.screen.display_card(self.player, card)

		util.cnt()

	def open_treasure(self):
		"""Gens Random Box and opens it"""

		terminal.clear()

		loot = random.choice(randomness.loot)

		if loot['type'] == 'weapon':
			w = weapon.generate_weapon()
			choice = self.screen.get_input(self.player, "You found a tier " + str(w.tier) + " " + str(w.name), [("Equip", 'equip'), ("Keep", 'keep'), ("Throw away", 'throw away')])

			if choice == 'equip':
				self.player.equip_weapon(w)
				self.player.store_weapon(w)

			elif choice == 'keep':
				self.player.store_weapon(w)

			else:
				self.screen.display_card(self.player, ["You threw away the " + w.name])
				util.cnt()

		elif loot['type'] == 'armor':
			a = armor.generate_armor()
			choice = self.screen.get_input(self.player, "You found a tier " + str(a.tier) + " " + str(a.name), [("Equip", 'equip'), ("Keep", 'keep'), ("Throw away", 'throw away')])

			if choice == 'equip':
				self.player.equip_armor(a)
				self.player.store_armor(a)

			elif choice == 'keep':
				self.player.store_armor(a)

			else:
				self.screen.display_card(self.player, ["You threw away the " + a.name])
				util.cnt()

		elif loot['type'] == 'health':
			self.screen.display_card(self.player, ["You found a " + loot['name']])
			health = random.randint(1, loot['max'])
			self.player.life += health
			if self.player.life > self.player.max_life:
				self.player.life = self.player.max_life
			util.cnt()

		elif loot['type'] == 'food':
			self.screen.display_card(self.player, ["You found a " + loot['name']])
			util.cnt()
			self.player.food.append(loot['name'])

		elif loot['type'] == 'gold':
			amount = random.randint(1, loot['max'])
			self.screen.display_card(self.player, ["You found " + str(amount) + " gold"])
			util.cnt()
			self.player.gold += amount

	
	def collect_shard(self):
		self.screen.display_card(self.player, ["You found a shard... A small glowing blue stone"])
		util.cnt()
		
		self.player.xp += 10
		self.player.shards += 1
		self.player.max_life += 10
		self.player.life += 10
		self.player.max_magic += 5
		self.player.magic += 5
	


	def win_game(self):
		"""Win game"""

		raw_prompts = [("Yes", "yes"), ("No", "no"), ("Not Sure", "no"), ("Nope", "no")]

		random.shuffle(raw_prompts)

		confirm = self.screen.get_input(self.player, "Are you sure you want to leave the dungeon?", raw_prompts=raw_prompts)

		if confirm == "yes":

			self.screen.display_card(content=["You left the dungeon with your gold", "You lived happily ever after...", "Or at least you tried, the enslaver is still alive...", "Each night the creatures keep coming...", "Until the enslaver is dead, these attacks will never end"])

			self.leaderboard.add_record(self.player)

			gamer_stats = f"""

		    Gold: {self.player.gold}
		    Depth Reached: {self.player.dungeon_level}
		    Level: {self.player.level}
		    
		    """

			with open("assets/gameover.txt", 'r') as file:
				self.screen.display_out(file.read()+gamer_stats)

			exit()

		else:
			return