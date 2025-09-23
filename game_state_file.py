import numpy as np
import card_file
import move_file
import piece_file

class game_state:
    def __init__(self, player_b_pieces:list[piece_file.piece], player_r_pieces:list[piece_file.piece], player_b_cards, player_r_cards, middle_card:card_file.card, is_b_turn:bool):
        self.player_b_pieces = player_b_pieces
        self.player_r_pieces = player_r_pieces
        self.player_b_cards = player_b_cards
        self.player_r_cards = player_r_cards
        self.middle_card = middle_card
        self.is_b_turn = is_b_turn


    def __get_all_occupied_squares(self,is_b=None): # by default func returns the coordinates of the pieces abt to go only
        if is_b == None and self.is_b_turn or is_b == True:
            return [piece.coordinates for piece in self.player_b_pieces]
        else:
             return [piece.coordinates for piece in self.player_r_pieces]
       


    def win_detection(self):
        pass
    def progress_game_state(self,move:move_file.move):
        pass
    def regress_game_state(self):
        pass

    def generate_possible_moves(self):
        occupied = self.__get_all_occupied_squares()
        if self.is_b_turn:
            moves = [current_piece.future_possible_moves for current_piece in self.player_b_pieces]
            flat_moves = [item for sublist in moves for item in sublist]
            return np.array([move for move in flat_moves if not(move.target in occupied)])
        else:
            moves = [current_piece.future_possible_moves for current_piece in self.player_r_pieces]
            flat_moves = [item for sublist in moves for item in sublist]# consider converting to np array than flattening for performance reasons
            return np.array([move for move in flat_moves if not(move.target in occupied)])
