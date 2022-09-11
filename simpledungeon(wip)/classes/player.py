from classes import armor, weapon
from code import util, terminal, randomness, screen
import random
import time


screen = screen.Screen()


class Player():
	def __init__(self):
		"""Initiate the Player"""

		# game data
		self.global_room_counter = 1

		# Life/Magic
		# EDIT: Stamina has been Removed
		self.life = 100
		self.max_life = 100
		self.magic = 10
		self.max_magic = 10
		self.has_magic = False

		# Level
		self.level = 1
		self.xp = 0
		self.max_xp = 15

		# Weapons/Armor
		self.weapon = weapon.Weapon("Fists", 1, 1, 1);
		self.armor = armor.Armor("Leather Tunic", 1)

		# Inventory/Money
		self.inventory = []
		self.weapons = [self.weapon]
		self.armors = [self.armor]
		self.loot = []
		self.max_weapons = 3
		self.max_armors = 3
		self.shards = 0
		self.gold = 0

		# Keep track of rooms played
		self.dungeon_level = 1

		# keep track of NPC stats
		self.npc_data = []

		# character
		self.character = ""
		self.give_boosts()

	def restore(self, dict):
		"""Restores the player from a dictionary"""


		# game data

		self.global_room_counter = dict['global_room_counter']

		# Life/Magic
		# EDIT: Stamina has been Removed
		self.life = dict['life']
		self.max_life = dict['max_life']
		self.magic = dict['magic']
		self.max_magic = dict['max_magic']
		self.has_magic = dict['has_magic']

		# Level
		self.level = dict['level']
		self.xp = dict['xp']
		self.max_xp = dict['max_xp']

		# Weapons/Armor
		self.weapon = weapon.weapon_from_dict(dict['weapon'])
		self.armor = armor.armor_from_dict(dict['armor'])

		# Inventory/Money
		self.inventory = dict['inventory']
		self.max_weapons = dict['max_weapons']
		self.max_armors = dict['max_armors']
		self.weapons = weapon.weapons_from_dict(dict['weapons'])
		self.armors = armor.armors_from_dict(dict['armors'])
		self.loot = dict['loot']
		self.shards = dict['shards']
		self.gold = dict['gold']

		# Keep track of rooms played
		self.dungeon_level = dict['dungeon_level']

		# Keep track of NPC data
		self.npc_data = dict['npc_data']

		# character
		self.character = dict['character']

	def give_boosts(self):
		"""Boost player according to character stats"""

		if self.character == "knight":
			self.life = 120
			self.max_life = 120
			self.has_magic = False
			self.armor = armor.Armor("Iron Armor", 3)
			self.weapon = weapon.Weapon("Broadsword", 4, 3, 7)

			self.weapons = [self.weapon]
			self.armors = [self.armor]

		elif self.character == 'archer':
			self.life = 75
			self.max_life = 75
			self.has_magic = False
			self.weapon = weapon.Weapon("Long Bow", 10, 5, 4)
			self.weapons = [self.weapon]

		elif self.character == 'wizard':
			self.life = 80
			self.max_life = 80
			self.magic = 30
			self.max_magic = 30
			self.weapon = weapon.Weapon("Ancient Staff", 10, 1, 5)
			self.weapons = [self.weapon]

		elif self.character == 'human':
			pass # nothing

		elif self.character == 'skeleton':
			self.has_magic = False
			self.weapon = weapon.Weapon("Cracked Bone", 1, 1, 1)
			self.weapons = [self.weapon]
			self.life = 50
			self.max_life = 50

	def level_up(self):
		if self.xp >= self.max_xp:
			self.level += 1
			self.xp = 0
			self.max_xp = int(self.max_xp*2.5)

			screen.display_card(self, ["LEVEL UP!"])
			input()

	def attack(self, enemy, buffs, enemies, noloot=False):
		"""Attack the Enemy and add Effects for Buffs"""

		terminal.clear()

		card = []

		raw_dmg = (self.weapon.damage+self.weapon.sharpness)*self.weapon.weight

		card.append(f"+{str(raw_dmg)}")


		dmg = (self.weapon.damage+util.floor(self.weapon.sharpness - enemy.armor.armor))*self.weapon.weight

		armor_block = raw_dmg-dmg

		card.append(f"   -{str(armor_block)} -- armor")

		for buff in buffs:
			if buff.dmg:
				dmg += buff.dmg
				if buff.dmg > 0:
					card.append(f"   +{buff.dmg} --{buff.reason}")
				else:
					card.append(f"   -{buff.dmg} --{buff.reason}")

		if dmg > 0:
			card.append(f" {str(dmg)} Damage")
		else:
			dmg = 0
			card.append(f" {str(dmg)} Damage")

		enemy.life -= dmg

		screen.display_card(self, card)

		util.cnt()

		if enemy.life <= 0:
			screen.display_card(self, ["You defeated the " + enemy.name])
			util.cnt()
			enemies.remove(enemy)
			if noloot:
				return
			else:
				self.loot_enemy(enemy)


			

	def loot_enemy(self, enemy):
		"""Loot the Enemy"""

		enemy.dead = True

		choice = screen.get_input(self, enemy.weapon.stats(), [("Keep", "keep"), ("Throw away", False)])

		if choice == 'keep':
			self.store_weapon(enemy.weapon)


		choice = screen.get_input(self, enemy.armor.stats(), [("Keep", "keep"), ("Throw away", False)])

		if choice == 'keep':
			self.store_armor(enemy.armor)
		

	
	def get_stats(self):
		"""Return Basic Player Stats"""
		if self.has_magic:
			return f"LIFE: {self.life}/{self.max_life} | MAGIC: {self.magic}/{self.max_magic} | GOLD: {self.gold}"
		else:
			return f"LIFE: {self.life}/{self.max_life} | GOLD: {self.gold} | DEPTH: {self.dungeon_level}"


	def shuffle_loadout(self):
		"""Shuffle Weapon and Armor Loadout"""
		while True:
			terminal.clear()

			loadout = [
				f"WEAPON: {self.weapon.name.capitalize()} DMG: {str(self.weapon.damage)} | SHRP: {str(self.weapon.sharpness)} | WGHT: {str(self.weapon.weight)} | TIER: {str(self.weapon.tier)}",
				f"ARMOR: {self.armor.name.capitalize()} ARMOR: {str(self.armor.armor)} | TIER: {str(self.armor.tier)}",
			]

			choice = screen.get_input(self, loadout, [("Equip Weapon", 1), ("Equip Armor", 2), ("Exit", 3)])
	
			if choice == 1:
				weapons = [f"{weapon.name} DMG: {weapon.damage} | SHRP: {weapon.sharpness} | WGHT: {weapon.weight} | TIER: {weapon.tier}" for weapon in self.weapons]	
				
				index = screen.get_input(self, "", [(weapon, weapons.index(weapon)) for weapon in weapons])
	
				self.equip_weapon(self.weapons[index])
	
			elif choice == 2:
				armors = [f"{armor.name} ARMOR: {armor.armor} | TIER: {armor.tier}" for armor in self.armors]
	
				index = screen.get_input(self, "", [(armor, armors.index(armor)) for armor in armors])
	
				self.equip_armor(self.armors[index])
	
			else:
				break

			util.cnt()

			
		

	def equip_weapon(self, weapon):
		"""Equip A Weapon"""
		self.weapon = weapon
		screen.display_card(self, [f"{self.weapon.name} equiped"])
		util.cnt()

	def store_weapon(self, weapon):
		"""Store A Weapon"""
		if len(self.weapons) >= 3:
			choice = screen.get_input(self, "Not enough space to store weapon!", [("Throw away", True), ("Replace a different weapon", False)])

			if choice:
				screen.display_card(self, ["You threw the " + weapon.name + " away"])
				util.cnt()

			else:
				weapons = []
				for w in self.weapons:
					weapons.append((f"{w.name} DMG: {str(w.damage)} | SHRP: {str(w.sharpness)} | WGHT: {str(w.weight)} | TIER: {str(w.tier)}", self.weapons.index(w)))

				choice = screen.get_input(self, "Choose a weapon to be replaced: ", weapons)

				self.weapons[choice] = weapon

				screen.display_card(self, ["Weapon stored."])
				util.cnt()
		else:
			self.weapons.append(weapon)
			screen.display_card(self, ["Weapon stored."])
			util.cnt()


	def equip_armor(self, armor):
		"""Equip Armor"""
		self.armor = armor
		screen.display_card(self, [f"{self.armor.name} equiped"])

	def store_armor(self, armor):
		"""Store Armor"""
		if len(self.armors) >= 3:
			choice = screen.get_input(self, "Not enough space to store armor!", [("Throw away", True), ("Replace a different armor", False)])

			if choice:
				screen.display_card(self, ["You threw the " + armor.name + " away"])
				util.cnt()

			else:
				armors = []
				for a in self.armors:
					armors.append((f"{a.name} ARMOR: {str(a.armor)} | TIER: {str(a.tier)}", self.armors.index(a)))

				choice = screen.get_input(self, "Choose an armor to be replaced: ", armors)

				self.armors[choice] = armor

				screen.display_card(self, ["Armor stored."])
				util.cnt()
		else:
			self.armors.append(armor)
			screen.display_card(self, ["Armor stored."])
			util.cnt()