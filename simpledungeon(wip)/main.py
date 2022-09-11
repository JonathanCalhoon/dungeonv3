from code import util, screen
from save_game import login_manager
from save_game import save

util.clear_log()

screen = screen.Screen()

screen.hide_cursor()

login = login_manager.LoginManager() #inits login

GAME = login.login() # Returns a game object

GAME.play() # runs the game object

screen.show_cursor()
