import random

class Armor():
    def __init__(self, name, armor, _type="armor"):
        """Initiate the Armor"""
        self.name = name
        self.armor = armor

        # Note: Removed Magic and Fire Armor stats
        # becuase they have little bearing on
        # real armor stats. 

        self._type = _type

        self.tier = int((self.armor*6)/10)

        # if cracked/rusted: remove armor and tier level due to cracked armor

    def stats(self):
        return f"{self.name.upper()} STRENGTH: {str(self.armor)} | TIER: {str(self.tier)}"


# WIP


armor = [
    # Orc's have terrible armor, they are not good craftsmen
    {
        "name" : "Orc's Armor",
        "armor" : (1, 3),
        "type" : "armor",
    },

    # Goblins have very good well made chain mail and armor
    {
        "name" : "Goblin's Chainmail",
        "armor" : (5, 8),
        "type" : "armor",
    },
    {
        "name" : "Goblin's Armor",
        "armor" : (6, 10),
        "type" : "armor",
    },

    # Kakavian Armor is Mid-Tier armor
    {
        "name" : "Kakavian Knight's Armor",
        "armor" : (4, 7),
        "type" : "armor",
    },
    {
        "name" : "Kakavian Chainmail",
        "armor" : (3, 6),
        "type" : "armor",
    },

    # Zigorian Armor/Cloaks/Chainmail is top tier

    {
        "name" : "Zigorian Chainmail",
        "armor" : (10, 10),
        "type" : "armor",
    },
    {
        "name" : "Zigorian Cloak",
        "armor" : (1, 1),
        "type" : "cloak",
        # cloaks will have some kind of stealth/magic/magic defense/etc effect
    },

    # RNG

    {
        "name" : "Leather Tunic",
        "armor" : (1, 1),
        "type" : "tunic",
    },
    {
        "name" : "Light Chainmail",
        "armor" : (2, 3),
        "type" : "tunic",
    },
    {
        "name" : "Boiled Leather Armor",
        "armor" : (1, 4),
        "type" : "armor",
    },
    {
        "name" : "Plate Armor",
        "armor" : (3, 7),
        "type" : "armor",
    },
    {
        "name" : "Scale Armor",
        "armor" : (3, 8),
        "type" : "armor",
    }
]

# END WIP


armor_class = ['cracked', 'thorgan', "knight's", "orc's", "goblin's", "rusty", "old", "new", "leather", "iron", "chainmail", "scale", "boiled leather", "mail", "plated mail", "plate"]
types = ['armor', 'cloak', 'shirt']

def generate_armor():
    """Generate a random set of armor"""

    _type = random.choice(types)

    armor = Armor(
        name=random.choice(armor_class) + " " + _type,
        armor = random.randint(1, 10),
        _type = _type,
    )

    return armor


def armor_from_dict(dict):
    """Builds Armor from Dict"""
    armor = Armor(
        name = dict['name'],
        armor = dict['armor'],
        _type = dict['_type'],
    )
    return armor

def armors_from_dict(list):
    """Builds Armor from List of Dict"""

    out = []

    for a in list:
        out.append(armor_from_dict(a))

    return out
