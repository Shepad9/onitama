import numpy as np
from time import sleep
import os
import game_file
import gui_file
import player_file

LOW_NOISE = 1
HIGH_NOISE = 3



def select_players():
    blue, red = gui_file.get_players()
    if blue == "diff1":
        blue = player_file.computer(True, noise = HIGH_NOISE)
    elif blue == "diff2":
        blue = player_file.computer(True, noise = LOW_NOISE)
    elif blue == "diff3":
        blue = player_file.computer(True)
    elif blue == "player":
        blue = player_file.player(True)
    if red == "diff1":
        red = player_file.computer(False, noise = HIGH_NOISE)
    elif red == "diff2":
        red = player_file.computer(False, noise = LOW_NOISE)
    elif red == "diff3": 
        red = player_file.computer(False)
    elif red == "player":
        red = player_file.player(False)
    
    return blue, red

def game_file_cycler(blue, red):
    for name in os.listdir("/home/shepad/projects/onitama/saves"):
        game = game_file.load_game(name, blue, red)
        if gui_file.is_correct_game_file():
            gui_file.game_display(game.current_game_state)
            return game
    return game_file_cycler(blue, red) # if all files passed on start again

def select_game_file(blue, red) -> game_file.game:
    if gui_file.get_game_file_type():
        return game_file.game.create_random_game(blue, red)
    return game_file_cycler(blue, red)
    
    




def main():
    blue, red = select_players()
    game = select_game_file(blue, red)
    game.play_game()

