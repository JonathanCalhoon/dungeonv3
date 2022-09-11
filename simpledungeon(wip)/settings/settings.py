import json
from code import terminal, util, screen
from getkey import getkey, keys


defualt = {
    "colors" : ["\u001b[34m"],
    'walls' : ' # ',
    'floor' : '   ',
    'empty' : ' . ',
    'treasure' : ' []',
    'player' : ' X ',
    'shards' : '\u001b[34m * \033[0m',
    'portal' : ' @ ',
    'play-spawn-animation' : True,
}

reset = "\033[0m"

class Settings():
    def __init__(self):
        self.build()
        self.screen = screen.Screen(colors=self.colors)

    def save(self, data=None):
        with open("settings/settings.txt", 'w') as file:
                file.write(json.dumps(
                {
                    "colors" : self.colors,
                    'walls' : self.walls,
                    'floor' : self.floor,
                    'empty' : self.empty,
                    'treasure' : self.treasure,
                    'player' : self.player,
                    'shards' : self.shards,
                    'portal' : self.portal,
                    'play-spawn-animation' : self.play_spawn,
                }))

    def build(self, data=None):
        """Check if Settings File has content, else Initiate Settings"""

        if not data:
            with open('settings/settings.txt', 'r') as file:
                data = json.loads(file.read())

            if not data:
                with open('settings/settings.txt', 'w') as file:
                    file.write(json.dumps(defualt))
                    data = defualt
        
        self.colors = data['colors']
        self.walls = data['walls']
        self.floor = data['floor']
        self.empty = data['empty']
        self.treasure = data['treasure']
        self.player = data['player']
        self.shards = data['shards']
        self.portal = data['portal']
        self.play_spawn = data['play-spawn-animation']



    def setup(self):
        """Change Settings around"""
        while True:
            prompts = []
            

    
            prompts.append((f"Walls: {self.walls}", 1))
            prompts.append((f"Floor: {self.floor}", 2))
            prompts.append((f"Empty: {self.empty}", 3))
            prompts.append((f"Treasure: {self.treasure}", 4))
            prompts.append((f"Player: {self.player}", 5))
            prompts.append((f"Shards: {self.shards}", 6))
            prompts.append((f"Portals: {self.portal}", 7))
            prompts.append(("Import Color Scheme", 8))
            prompts.append(("Export Color Scheme", 9))
            prompts.append((f"Play Spawn Animation? {self.play_spawn}", 10))
            prompts.append(("Exit", 11))

            choice = self.screen.get_input(raw_prompts=prompts)
    
            if choice == 1:
                self.walls = self.change_settings()
            elif choice == 2:
                self.floor = self.change_settings()
            elif choice == 3:
                self.empty = self.change_settings()
            elif choice == 4:
                self.treasure = self.change_settings()
            elif choice == 5:
                self.player = self.change_settings()
            elif choice == 6:
                self.shards = self.change_settings()
            elif choice == 7:
                self.portal = self.change_settings()
            elif choice == 8:
                self.screen.display_card(content=["Copy JSON: ", str({'walls' : self.walls,'floor' : self.floor,'empty' : self.empty,'treasure' : self.treasure,'player' : self.player,'shards' : self.shards,'portal' : self.portal, 'play-spawn-animation' : self.play_spawn})])
                util.cnt()
            elif choice == 9:
                try:
                    new_json = json.loads(input("JSON: "))
                    self.build(new_json)
                except:
                    self.screen.display_card(content=["JSON not valid!"])
                    util.cnt()
            elif choice == 10:
                if not self.play_spawn:
                    self.play_spawn = True
                else:
                    self.play_spawn = False
            else:
                self.build({'colors': self.colors, 'walls' : self.walls,'floor' : self.floor,'empty' : self.empty,'treasure' : self.treasure,'player' : self.player,'shards' : self.shards,'portal' : self.portal, 'play-spawn-animation' : self.play_spawn})
                self.save()
                return

    def get_color(self):
        """Get a color"""
        color = 0
        while True:
            terminal.clear()
            your_color = f"\033[{color}m"
            print(f"Your Color: {your_color}{ascii(your_color)}\033[0m")

            control = getkey()

            if control == 'w' or control == keys.UP:
                color += 1
            elif control == 's' or control == keys.DOWN:
                if color - 1 >= 0:
                    color -= 1
            elif control == '\n':
                return your_color





    def change_settings(self):
        """Change a setting"""

        fg = "\033[0m"
        bg = "\033[0m"
        char = "   "
        while True:
            choice = self.screen.get_input(question=f"Current: {fg+bg+char+reset}", raw_prompts=[("Change FG Color", 1), ("Change BG Color", 2), ("Change Character", 3), ("Exit", 4)])


            if choice == 1:
                color = self.get_color()
                if color not in self.colors:
                    self.colors.append(color)
                fg = color


            elif choice == 2:
                color = self.get_color()
                if color not in self.colors:
                    self.colors.append(color)
                bg = color


            elif choice == 3:
                character = input(">>> ")
                if len(character) == 1:
                    char = " "+character+" "
                elif len(character) == 3:
                    char = character
                else:
                    print("Must be 1 or 3 characters.")

            else:
                return fg+bg+char+reset






                
    
    
    
    
    
    
    
            

        


        