import numpy as np
import game_file
import gui_file
import player_file


def play_new_game(blue, red): # add difficulty as a input
    game  = game_file.game.create_random_game(blue(True), red(False))
    game.play_game()

def play_saved_game(name, blue, red):
    game = game_file.load_game(name, blue(True), red(False))
    game.play_game

def select_players():
    pass

def select_game_file():
    pass