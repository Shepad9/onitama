import json
import numpy as np
import os
import random
import pandas as pd
from copy import deepcopy
from sys import exit
from time import time, sleep
import move_file
import game_state_file
import piece_file
import card_file
import player_file
import gui_file
import review_file
import matplotlib.pyplot as plt


MOVES_TO_UNDO = 1 
TIME_FOR_WIN = 1


class game:
    def __init__(self, current_game_state:game_state_file.game_state, initial_game_state:game_state_file.game_state, player_b:player_file.player, player_r:player_file.player, move_stack:list[move_file.move] = []):
        self.current_game_state = current_game_state
        self.initial_game_state = initial_game_state
        self.player_b = player_b
        self.player_r = player_r
        self.move_stack = move_stack

    def create_random_game(blue, red):
        g = game_state_file.create_random_game_state()
        g1 = deepcopy(g)
        gui_file.game_display(g)
        if type(blue) != player_file.computer and type(blue) != player_file.computer:
            MOVES_TO_UNDO = 1
        return game(g, g1, blue, red)



    def __get_active_player(self) -> player_file.player:
        if self.current_game_state.is_b_turn:
            return self.player_b
        else:
            return self.player_r

    def play_game(self): 
        
        while self.current_game_state.is_game_live: 
            move = self.__get_active_player().get_move(self.current_game_state) # get move
            if type(move) == str:
                if move == "save_command":
                    self.save_game()
                elif move == "undo_command":
                    self.undo()
                elif move == "hint_command":
                    move = self.hint()
                elif move == "move_command":
                    move = self.full_hint()
                elif move == "instructions_command":
                    temp = gui_file.instructions_display()
                    self.play_game()
            
                else:
                    raise Exception("unrecognised internal message")
            else:
                self.move_stack.append(move)   
                self.current_game_state.progress_game_state(move) # progress game_state
            gui_file.game_display(self.current_game_state)
        self.game_over()
        
    def play_game_SRC(self): #  test progress game_state
        
        src = []
        game_progression = []
        while self.current_game_state.is_game_live:
            move = self.__get_active_player().get_move(self.current_game_state)
            game_progression.append(len(self.move_stack))
            src.append(SRCS(self.current_game_state))
            self.move_stack.append(move)
            self.current_game_state.progress_game_state(move) # progress game_state
            gui_file.game_display(self.current_game_state)
        self.show_graph(src, game_progression)

    def show_graph(self, src, game_progression):
        plt.plot(game_progression, src)
        plt.savefig("/home/shepad/projects/onitama/src_over_time/test_1.png")

    def game_over(self):
        sleep(TIME_FOR_WIN)
        if gui_file.should_review(self.current_game_state.is_b_turn):
            self.review()
        else:
            main()

    def review(self):
        review_obj = review_file.review(self.initial_game_state, self.move_stack)
        review_obj.review()
        main()
    def save_game(self): # assume files in objecr form

        cards = [self.initial_game_state.player_b_cards[0].name,self.initial_game_state.player_b_cards[1].name,self.initial_game_state.player_r_cards[0].name,self.initial_game_state.player_r_cards[1].name,self.initial_game_state.middle_card.name]
        moves = list([move_to_dict(move) for move in self.move_stack])
        thing_to_save = {"cards": cards, "moves": moves}
        with open (f"saves/{str(time())}.txt","x") as outfile:
            json.dump(thing_to_save,outfile)
            outfile.close()
        main()
    

    def undo(self):
        
        self.current_game_state = deepcopy(self.initial_game_state)
        self.move_stack = self.move_stack[:- MOVES_TO_UNDO]
        for move in self.move_stack:
            self.current_game_state.progress_game_state(move) # remove  from move stack chamge current game state

    def hint(self) -> move_file.move:
        com = player_file.computer(self.current_game_state.is_b_turn)
        hint_move = com.get_move(self.current_game_state)
        gui_file.game_display(self.current_game_state, hint_source=hint_move.source)
        self.play_game()

    def full_hint(self) -> move_file.move:
        com = player_file.computer(self.current_game_state.is_b_turn)
        hint_move = com.get_move(self.current_game_state)
        gui_file.game_display(self.current_game_state, hint_source=hint_move.source, hint_target= hint_move.target)
        self.play_game()





def reconstruct_ini_state(cards):
    b_pieces = piece_file.piece.create_pieces(5,[(-2,0),(-2,-2),(-2,-1),(-2,1),(-2,2)],[True,True,True,True,True],[True,False,False,False,False])
    r_pieces = piece_file.piece.create_pieces(5,[(2,0),(2,-2),(2,-1),(2,1),(2,2)],[False,False,False,False,False],[True,False,False,False,False])
    g = game_state_file.game_state(b_pieces,r_pieces,[cards[0],cards[1]],[cards[2],cards[3]],cards[4],cards[4].is_stamp_blue) 
    for piece in g.player_b_pieces:
        piece.future_possible_moves = piece.next_moves(g.player_b_cards)#use this to update all cards future possible moves in actual code
    for piece in g.player_r_pieces:
        piece.future_possible_moves = piece.next_moves(g.player_r_cards)
    return g


def move_to_dict(move):
    return {"card":move.card.name, "target":move.target, "source":move.source}#we only take the coords of piece
def dict_to_move(dict):
    card = card_file.card.create_card(dict["card"])
    target = tuple(dict["target"])
    source = tuple(dict["source"])
    return move_file.move(card, target, source)

 
def create_game(g, blue, red) -> game:
    g1 = deepcopy(g)
    return game(g, g1, blue, red)

def load_game(name, blue = player_file.player(True), red = player_file.player(False), folder = "saves") -> game:
    with open(f"/home/shepad/projects/onitama/{folder}/{name}") as infile:
        game_string = json.load(infile)
        cards, dict_moves = game_string["cards"], game_string["moves"]
        infile.close()
    initial_state = reconstruct_ini_state([card_file.card.create_card(card) for card in cards])
    game = create_game(initial_state, blue, red)
    moves = [dict_to_move(temp) for temp in dict_moves] # converts the json dict back to object form
    for move in moves:
        game.current_game_state.progress_game_state(move)
    game.move_stack = moves
    gui_file.game_display(game.current_game_state, is_file_cycling = True)
    return game

TEST_ACCURACY = 10
MAX_MOVES_FOR_RANDOM = 15
STAT_MAX = 300

def SRCS(g1):
    com_b = player_file.computer(True)
    com_r = player_file.computer(False)
    
    
    if g1.is_b_turn:
        stat = com_b.quiescence_max(g1)
        dyna = com_b.maximiser(g1)["score"]
    else:
        stat = com_r.quiescence_min(g1)
        dyna = com_r.minimiser(g1)["score"] 
    return  abs((stat - dyna) / STAT_MAX)



def SRCS_avg():
    
    game_states = []

    for i in range(TEST_ACCURACY):
        g = game.create_random_game(player_file.full_random(True), player_file.full_random(False))
        for i in range (random.randint(3,MAX_MOVES_FOR_RANDOM)):

            move = g._game__get_active_player().get_move(g.current_game_state)
            g.move_stack.append(move)   
            g.current_game_state.progress_game_state(move) # get move
        if g.current_game_state.is_game_live:
            game_states.append(g.current_game_state)
    vectorized_SRCS = np.vectorize(SRCS)

    return sum(vectorized_SRCS(np.array(game_states))) / TEST_ACCURACY

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
        game = load_game(name, blue, red)
        if gui_file.is_correct_game_file():
            gui_file.game_display(game.current_game_state)
            return game
    return game_file_cycler(blue, red) # if all files passed on start again

def select_game_file(blue, red) -> game:
    if gui_file.get_game_file_type():
        return game.create_random_game(blue, red)
    return game_file_cycler(blue, red)
    
    




def main():
    blue, red = select_players()
    game = select_game_file(blue, red)
    game.play_game()

def record_src_over_time():
    blue, red = player_file.computer(True), player_file.computer(False)
    gprime = game.create_random_game(blue, red)
    gprime.play_game_SRC()

