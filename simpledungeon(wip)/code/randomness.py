import random
import copy

loot = [
    {"type":"health","name":"Drop of Health", "max":2},
    {"type":"health","name":"Small vial of Health", "max":5},
    {"type":"health","name":"Vial of Health", "max":15},
    {"type":"health","name":"Flask of Health", "max":20},
    {"type":"health","name":"Bottle of Health", "max":40},
    {"type":"health","name":"Wineskin of Health", "max":100},
    {"type":"armor", "name":"", "max":1},
    {"type":"weapon", "name":"", "max":1},
    {"type":"gold", "name":"", "max":25},
    {"type":"gold", "name":"", "max":25},
    {"type":"gold", "name":"", "max":25},
    {"type":"gold", "name":"", "max":25},
    {"type":"gold", "name":"", "max":25},
    {"type":"gold", "name":"", "max":25},
    {"type":"gold", "name":"", "max":25},
    {"type":"gold", "name":"", "max":25},
    {"type":"gold", "name":"", "max":25},
]


valid_potions = ['potion of energy', 'healing potion']

valid_spells = ['sana ego', 'sana vulnera', 'sana omnis ego', 'confirma impetum', 'confirma defensio', 'noxa hostilis']


enemy_symbols = ['S', 'G', 'g', 'T', 'W']


character_symbols = ['R', 'D', "L"]




knight = """
----------
|   __   |
|  [--]  |
| \/||\} |
|   /\   |
----------""".split("\n")

archer = """
------------
|  __      |
| (OO)|\   |
| \||-||-> |
|  /\ |/   |
------------""".split("\n")

wizard = """
--------
|  __  |
| (**) |
| //\\\ |
| /__\ |
--------""".split("\n")

human = """
--------
|  __  |
| (oo) |
| /||\ |
|  /\  |
--------""".split("\n")

skeleton = """
--------
|  __  |
| (xx) |
| /][\ |
|  /\  |
--------""".split("\n")

def get_char(player):
    if player.character == "knight":
        return copy.deepcopy(knight)
    elif player.character == "archer":
        return copy.deepcopy(archer)
    elif player.character == "wizard":
        return copy.deepcopy(wizard)
    elif player.character == "human":
        return copy.deepcopy(human)
    elif player.character == "skeleton":
        return copy.deepcopy(skeleton)