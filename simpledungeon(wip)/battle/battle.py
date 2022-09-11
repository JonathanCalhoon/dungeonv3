from code import terminal, util, randomness, screen
from battle import die, completer
import random
import time

screen = screen.Screen()


def living_enemies(enemies):
	"""Check if any enemies are still alive"""
	val = False
	for enemy in enemies:
		if enemy.life > 0:
			val = True

	return val


def fight(player, enemies):
	"""Fight between Player and Enemy"""
	if type(enemies) != list:
		enemies = [enemies]

	player_turn = True # Todo: Switch this to calc for speed stats

	valid_nums = [str(i) for i in range(0, 9)]

	buffs = []

	last_hit = None

	green = "\033[32m"
	red = "\033[31m"
	reset = "\033[0m"

	while player.life > 0 and living_enemies(enemies) > 0:
		while player_turn:
			terminal.clear()

			prompt = []
			prompt.append("")
			prompt.append("")
			prompt.append("---------- BUFFS -----------")
			prompt.append("")
			for b in buffs:
				if not b.enemy:
					prompt.append(f"{red}{b.reason} -> {b.des}{reset}")
				else:
					prompt.append(f"{green}{b.reason} -> {b.des}{reset}")
			if not buffs:
				prompt.append("None")
			prompt.append("")
			prompt.append("------------------------------")
			prompt.append("")
			prompt.append("")
			prompt.append("---------- ENEMIES -----------")
			prompt.append("")
			for enemy in enemies:
				prompt.append(f"[{str(enemies.index(enemy))}] {enemy.name} -> Life:  {str(enemy.life)}")
			prompt.append("")
			prompt.append("------------------------------")
			prompt.append("")
			prompt.append("")


			command_list = ["drink healing potion", "drink potion of energy", "loadout", "run", "?", "help"]

			if player.has_magic:
				command_list += ["magicae sana vulnera", "magicae sana ego", "magicae confirma defensio", "magicae confirma impetum", "magicae noxa hostilis"]

			for i in range(len(enemies)):
				command_list.append("attack " + str(i))

			c = completer.Completer(command_list, prompt, player)

			commands = ['?', 'help', 'attack', 'loadout', 'drink', 'magicae', 'run']

			full = c.get_input()

			if full:
				c = full.split()
				command = c[0]
			else:
				command = None

			if command in commands:
				# use try to invalid commands
				if command == '?' or command == 'help':
					card = []
					card.append("Commands: \n")
					card.append("attack <target> | Example: attack 0")
					card.append("loadout | Change Weapons/Armor")
					card.append("drink <potion> | Example: drink healing potion")
					card.append("magicae <spell> | Example: magicae sana vulnera")
					card.append("run | Warning: You may be killed")
					screen.display_card(card)
				
				elif command == 'attack':
					try:
						target = c[1]
					except:
						target = "0"

					if target in valid_nums:
						enemy = enemies[int(target)]
						player.attack(enemy, buffs, enemies)
						last_hit = enemy
						player_turn = False
				
				elif command == 'loadout':
					player.shuffle_loadout()
				
				elif command == 'run':
					if random.randint(1, 4) == 1:
						die.die(player, "Struck in the back while running like a coward.")
					else:
						screen.display_card(player, ["You flee the battle"])
						return
				
				elif command == 'drink':
					try:
						potion = " ".join(c[1:]).lower()
					except:
						potion = ""
						screen.display_card(player, ["You did not specify a potion! Type help or ? to see commands"])

					if potion in player.food and potion in randomness.valid_potions:
						player.food.remove(potion)
						
						if potion == 'potion of energy':
							b = buff.Buff(50, 0, 1, "Potentia Navitas", "+50 on next attack")
							screen.display_card(player, ["Buff Activated: +50 on next attack"])
							buffs.append(b)
						elif potion == 'healing potion':
							screen.display_card(player, ["You drank the healing potion..."])
							player.life = player.max_life
						player_turn = False
					else:
						screen.display_card(player, ["You don't have that potion!"])
				
				elif command == 'magicae':
					try:
						spell = " ".join(c[1:])
					except:
						spell = ""
						screen.display_card(player, ["You did not specify a spell! Type help or ? to see commands"])
					if spell in randomness.valid_spells:
						if spell == 'sana ego':
							if player.magic >= 4:
								player.magic -= 4
								player.life += 10
								if player.life > player.max_life:
									player.life = player.max_life
							else:
								screen.display_card(player, ["You do not have enough power to throw that spell"])

						elif spell == 'sana vulnera':
							if player.magic >= 5:
								player.magic -= 5
								player.life += 15
								if player.life > player.max_life:
									player.life = player.max_life
							else:
								screen.display_card(player, ["You do not have enough power to throw that spell"])
						
						elif spell == 'sana omnis vulnera':
							if player.magic >= 10:
								player.magic -= 10
								player.life += 40
								if player.life > player.max_life:
									player.life = player.max_life
							else:
								screen.display_card(player, ["You do not have enough power to throw that spell"])
						
						elif spell == 'confirma impetum':
							if player.magic >= 10:
								player.magic -= 10
								b = buff.Buff(40, 0, 1, ["Confirma Impetum", "+40 Damage on Next Attack"])
								buffs.append(b)
								screen.display_card(player, ["Buff Activated: +40 Damage on Next Attack"])
							else:
								screen.display_card(player, ["You do not have enough power to throw that spell"])
						
						elif spell == 'confirma defensio':
							if player.magic >= 10:
								player.magic -= 10
								b = buff.Buff(0, -40, 1, ["Confirma Defensio", "-40 Damage On Next Enemy Attack"])
								buffs.append(b)
								screen.display_card(player, ["Buff Activated: -40 Damage on Next Enemy Attack"])
							else:
								screen.display_card(player, ["You do not have enough power to throw that spell"])
						
						elif spell == 'noxa hostilis':
							if player.magic >= 25:
								player.magic -= 25
								screen.display_card(player, ["All Enemies Recieve 50 Damage"])
								for enemy in enemies:
									enemy.life -= 50
									if enemy.life <= 0:
										enemies.remove(enemy)
										player.loot_enemy(enemy)
							else:
								screen.display_card(player, ["You do not have enough power to throw that spell"])
					else:
						screen.display_card(player, ["Your strange magic words are confusing..."])
						screen.display_card(player, [spell + " is not a spell"])

		

		while not player_turn:
			player_turn = True
			terminal.clear()
			for enemy in enemies:
				card = []

				raw_dmg = (enemy.weapon.damage+enemy.weapon.sharpness)*enemy.weapon.weight

				card.append(f"+{str(raw_dmg)}")

				dmg = (enemy.weapon.damage+util.floor(enemy.weapon.sharpness - player.armor.armor))*enemy.weapon.weight

				armor_block = raw_dmg-dmg

				card.append(f"   -{str(armor_block)} -- armor")

				if dmg > 0:
					card.append(f" {str(dmg)} Damage")
				else:
					dmg = 0
					card.append(f" {str(dmg)} Damage")

				player.life -= dmg

				screen.display_card(player, card)

				input()

				if player.life <= 0:
					die.die(player, f"slaughtered by a {enemy.name} in battle")
							