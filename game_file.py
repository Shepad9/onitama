import numpy as np
import move_file
import game_state_file
import piece_file
import card_file

class game:
    def __init__(self, current_game_state, initial_game_state, player_b, player_r, move_stack = []):
        self.current_game_state = current_game_state
        self.initial_game_state = initial_game_state
        self.player_b = player_b
        self.player_r = player_r
        self.move_stack = move_stack

    def create_random_game(blue,red):
        b_pieces = piece_file.piece.create_pieces(5,[(-2,0),(-2,-2),(-2,-1),(-2,1),(-2,2)],[True,True,True,True,True],[True,False,False,False,False])
        r_pieces = piece_file.piece.create_pieces(5,[(2,0),(2,-2),(2,-1),(2,1),(2,2)],[False,False,False,False,False],[True,False,False,False,False])
        cards = card_file.card.create_5_random_cards()
        g = game_state_file.game_state(b_pieces,r_pieces,[cards[0],cards[1]],[cards[2],cards[3]],cards[4],True) #write some code to determine who moves first
        g.b_pieces = [piece.next_moves(g.player_b_cards) for piece in g.player_b_pieces] #use this to update all cards future possible moves in actual code
        g.r_pieces = [piece.next_moves(g.player_r_cards) for piece in g.player_r_pieces]
        return game(g, g, blue, red)


    def __get_active_player(self):
        if self.current_game_state.is_b_turn:
            return self.player_b
        else:
            return self.player_r

    def play_game(self): #  test progress game_state
        while self.current_game_state.is_game_live == True:
            move = self.__get_active_player.get_move(self.current_game_state) # get move
            self.current_game_state.progress_game_state(move) # progress game_state
            self.move_stack.append(move)
        print("winner is",self.current_game_state.is_b_turn)

