from code import screen, terminal, util


screen = screen.Screen()


def die(player, reason):
    """Die"""
    death_screen = f"""
      @@@@@@@@@@@@@@@@@@
     @@@@@@@@@@@@@@@@@@@@@@@
   @@@@@@@@@@@@@@@@@@@@@@@@@@@
  @@@@@@@@@@@@@@@@@@@@@@@@@@@@@
 @@@@@@@@@@@@@@@/      \\@@@/   @
@@@@@@@@@@@@@@@@\\      @@  @___@
@@@@@@@@@@@@@ @@@@@@@@@@  | \@@@@@
@@@@@@@@@@@@@ @@@@@@@@@\\__@_/@@@@@
 @@@@@@@@@@@@@@@/,/,/./'/_|.\\'\\,\\
   @@@@@@@@@@@@@|  | | | | | | | |
                 \\_|_|_|_|_|_|_|_|

    {reason}
"""
    screen.display_card(player, death_screen.split("\n"))

    util.cont()

    terminal.clear()


    gamer_stats = f"""

    Gold: {player.gold}
    Depth Reached: {player.dungeon_level}
    Level: {player.level}
    
    """

    with open("assets/gameover.txt", 'r') as file:
        screen.display_out(file.read()+gamer_stats)

    exit()