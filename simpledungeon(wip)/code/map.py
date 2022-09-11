import random, time
from code import util, randomness, screen
from generators import monsters


screen_size = 10

screen = screen.Screen()


#width is 65 counting borders
#actual width is 63




def animate_entry(dungeon, x, y, settings, stats):
    """Show the portal open and disappear as the player enters"""

    if not settings.play_spawn:
        return

    dungeon[y][x] = '@'


    delay = .5
    base_map = build_display_map(dungeon, x, y)

    for row in base_map:
        if '@' in row:
            y = base_map.index(row)
            for i in row:
                if i == '@':
                    x = row.index(i)

    base_map[y][x] = '.'

    display(settings, base_map, x, y, stats, noplace=True)

    time.sleep(delay)

    base_map[y][x] = '@'

    display(settings, base_map, x, y, stats, noplace=True)

    time.sleep(delay)

    base_map[y+1][x] = '.'
    base_map[y-1][x] = '.'
    base_map[y][x+1] = '.'
    base_map[y][x-1] = '.'

    display(settings, base_map, x, y, stats, noplace=True)

    time.sleep(delay)

    base_map[y][x] = 'p'

    display(settings, base_map, x, y, stats, noplace=True)

    time.sleep(delay)








def build_display_map(dungeon, x, y):
    """Cuts the full map into a size based on the users location"""
    # TODO: Fix this crap
    display_map = []
    for i in range(-screen_size, screen_size):
        try:
            display_map.append(dungeon[y+i])
        except:
            display_map.append(["."]*screen_size)
    final = []
    for row in display_map:
        new_row = []
        for i in range(-screen_size+x, screen_size+1+x):
            try:
                new_row.append(row[i])
            except:
                new_row.append(".")
                
        final.append(new_row)
    return final
    
    

def display(settings, dungeon, x, y, stats=[], noplace=False):
    """Display the dungeon"""
    print("\033[H",end="")
    if not noplace:
        dungeon[y][x] = 'p'

    _map = build_display_map(dungeon, x, y)

    out_list = []

    out_list.append("---"*21+"--")
    for stat in stats:
        count = int((60-len(stat))/2)
        _str = "|  " + (" "*count) + stat + (" "*count)
        if len(_str) == 62:
            _str += "  |"
        else:
            _str += " |"

        out_list.append(_str)

        
    out_list.append("---"*21+"--")
    for row in _map:
        r = "|"
        for cell in row:
            if cell == 't':
                r += settings.treasure
            elif cell == '*':
                r += settings.shards
            elif cell == 'p':
                r += settings.player
            elif cell == '#':
                r += settings.walls
            elif cell == '.':
                r += settings.empty
            elif cell == ' ':
                r += settings.floor
            elif cell == '@':
                r += settings.portal
            else:
                r += " "+cell+" "
        out_list.append(r+"|")
    out_list.append("---"*21+"--")
    out_list.append(util.center(" 1. View Stats | 2. Change Loadout | 3. Save", 65))
    out_list.append(util.center(" 4. Clear Screen | 5. Display Settings", 65))

    screen.display_out(out_list)
  

def getSpawn(dungeon):
    """Spawn the player somewhere in the dungeon"""
    valid = False
    while True:
        y = random.randint(0, len(dungeon)-1)
        if " " in dungeon[y]:
            while True:
                x = random.randint(0, len(dungeon[y])-1)
                if dungeon[y][x] == ' ':
                    return y, x


def place_rand_object(dungeon, obj):
    """Place an Object in a random location somewhere in the dungeon"""
    valid = False
    while True:
        y = random.randint(0, len(dungeon)-1)
        if " " in dungeon[y]:
            while True:
                x = random.randint(0, len(dungeon[y])-1)
                if dungeon[y][x] == ' ':
                    dungeon[y][x] = obj
                    return (y, x)