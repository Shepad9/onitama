import numpy as np
import card_file
import move_file
import piece_file


class game_state:
    def __init__(self, player_b_pieces:list[piece_file.piece], player_r_pieces:list[piece_file.piece], player_b_cards, player_r_cards, middle_card:card_file.card, is_b_turn:bool,is_game_live = True):
        self.player_b_pieces = player_b_pieces
        self.player_r_pieces = player_r_pieces
        self.player_b_cards = player_b_cards
        self.player_r_cards = player_r_cards
        self.middle_card = middle_card
        self.is_b_turn = is_b_turn
        self.is_game_live = is_game_live

    


    def create_game_state(b_pieces,r_pieces,b_cards,r_cards,m_card,is_b):
        return game_state(b_pieces,r_pieces,b_cards,r_cards,m_card,is_b)

    

    def __get_all_occupied_squares(self,is_b=None): # by default func returns the coordinates of the pieces abt to go only
        if is_b == None and self.is_b_turn or is_b == True:
            return [piece.coordinates for piece in self.player_b_pieces]
        else:
             return [piece.coordinates for piece in self.player_r_pieces]
    def __get_master_coordinates(self,is_b=None):# returns None if master not found
        if (is_b == None and self.is_b_turn) or is_b == True:
            coords = [piece.coordinates for piece in self.player_b_pieces if piece.is_master == True]
        else:
            coords = [piece.coordinates for piece in self.player_r_pieces if piece.is_master == True]
        if len(coords) > 1:
            raise Exception("can only be 1 master")
        elif len(coords) == 1:
            return coords[0]
        else:
            return None



    def is_win(self,is_b = None):
        if is_b == None:
            is_b = self.is_b_turn
        if is_b == True:
            return self.__get_master_coordinates(not(is_b)) == None or self.__get_master_coordinates(is_b) == (2,0)
        else:
            return self.__get_master_coordinates(not(is_b)) == None or self.__get_master_coordinates(is_b) == (-2,0)
    def update_is_game_live(self):
        if self.is_win():
            self.is_game_live = False



    def progress_game_state(self,move:move_file.move):
        # update piece coords
        move.piece.coordinates = move.target
        # check to see if a piece must be deleted
        if self.is_b_turn:
            self.player_r_pieces = [opposition_piece for opposition_piece in self.player_r_pieces if opposition_piece.coordinates != move.piece.coordinates]
        else:
            self.player_b_pieces = [opposition_piece for opposition_piece in self.player_b_pieces if opposition_piece.coordinates != move.piece.coordinates]
        # win detection
        self.update_is_game_live()
        # swap cards
        if self.is_b_turn:
            self.player_b_cards.remove(move.card)
            self.player_b_cards.append(self.middle_card)
        else:
            self.player_r_cards.remove(move.card)
            self.player_r_cards.append(self.middle_card)
         
        self.middle_card = move.card
        # generate new future possible moves
        if self.is_b_turn:
            move.piece.future_possible_moves = move.piece.next_moves(self.player_b_cards)
            for piece in self.player_b_pieces:
                piece.future_possible_moves = piece.add_card(self.player_b_cards[1])
        else:
            move.piece.future_possible_moves = move.piece.next_moves(self.player_r_cards)
            for piece in self.player_r_pieces:
                piece.future_possible_moves = piece.add_card(self.player_r_cards[1])
        # pass play to opposition
        self.is_b_turn = not(self.is_b_turn)
        
    def regress_game_state(self):
        pass

    def generate_possible_moves(self):
        occupied = self.__get_all_occupied_squares()
        if self.is_b_turn:
            moves = [current_piece.future_possible_moves for current_piece in self.player_b_pieces]
            flat_moves = [item for sublist in moves for item in sublist]
            return np.array([move for move in flat_moves if not(move.target in occupied) and move.card in self.player_b_cards])
        else:
            moves = [current_piece.future_possible_moves for current_piece in self.player_r_pieces]
            flat_moves = [item for sublist in moves for item in sublist]# consider converting to np array than flattening for performance reasons
            return np.array([move for move in flat_moves if not(move.target in occupied) and move.card in self.player_r_cards])
    
    def display(self): #temporary before gui
        for card in self.player_b_cards:
            card.display()
        
         
        for card in self.player_r_cards:
            card.display()
        print("is is blue turn", self.is_b_turn)
        print("middle card")
        self.middle_card.display()
