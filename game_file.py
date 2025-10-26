import json
from copy import deepcopy
from sys import exit
from time import time
import move_file
import game_state_file
import piece_file
import card_file
import player_file
import gui_file


MOVES_TO_UNDO = 2

class game:
    def __init__(self, current_game_state:game_state_file.game_state, initial_game_state:game_state_file.game_state, player_b:player_file.player, player_r:player_file.player, move_stack:list[move_file.move] = []):
        self.current_game_state = current_game_state
        self.initial_game_state = initial_game_state
        self.player_b = player_b
        self.player_r = player_r
        self.move_stack = move_stack

    def create_random_game(blue, red):
        g = game_state_file.create_random_game_state()
        gui_file.game_display(g)
        g1 = deepcopy(g)    
        return game(g, g1, blue, red)



    def __get_active_player(self):
        if self.current_game_state.is_b_turn:
            return self.player_b
        else:
            return self.player_r

    def play_game(self): #  test progress game_state
       
        while self.current_game_state.is_game_live == True:
            move = self.__get_active_player().get_move(self.current_game_state) # get move
            if type(move) == str:
                if move == "save_command":
                    self.save_game()
                elif move == "undo_command":
                    self.undo()
                else:
                    raise Exception("unrecognised internal message")
            else:
                self.move_stack.append(move)   
                self.current_game_state.progress_game_state(move) # progress game_state
            gui_file.game_display(self.current_game_state)
            
            
        print("winner is",not(self.current_game_state.is_b_turn))
        print(self.move_stack)

    def save_game(self): # assume files in objecr form

        cards = [self.initial_game_state.player_b_cards[0].name,self.initial_game_state.player_b_cards[1].name,self.initial_game_state.player_r_cards[0].name,self.initial_game_state.player_r_cards[1].name,self.initial_game_state.middle_card.name]
        moves = list([move_to_dict(move) for move in self.move_stack])
        thing_to_save = {"cards": cards, "moves": moves}
        with open (f"saves/{str(time())}.txt","x") as outfile:
            json.dump(thing_to_save,outfile)
            outfile.close()
        exit("file has been created name")

    def undo(self):
        
        self.current_game_state = deepcopy(self.initial_game_state)
        self.move_stack = self.move_stack[:- MOVES_TO_UNDO]
        for move in self.move_stack:
            self.current_game_state.progress_game_state(move) # remove  from move stack chamge current game state




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

def load_game(name, blue, red):
    with open(f"saves/{name}.txt") as infile:
        game_string = json.load(infile)
        cards, dict_moves = game_string["cards"], game_string["moves"]
        infile.close()
    initial_state = reconstruct_ini_state([card_file.card.create_card(card) for card in cards])
    game = create_game(initial_state, blue, red)
    moves = [dict_to_move(temp) for temp in dict_moves] # converts the json dict back to object form
    for move in moves:
        game.current_game_state.progress_game_state(move)
    game.move_stack = moves
    gui_file.game_display(game.current_game_state)
    return game


    



