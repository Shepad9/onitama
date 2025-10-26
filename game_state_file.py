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


    def __get_all_occupied_squares(self,is_b=None): # by default func returns the coordinates of the pieces abt to go only
        if is_b == None and self.is_b_turn or is_b == True:
            return [piece.coordinates for piece in self.player_b_pieces]
        else:
             return [piece.coordinates for piece in self.player_r_pieces]
    def get_master_coordinates(self,is_b=None):# returns None if master not found
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
            return self.get_master_coordinates(not(is_b)) == None or self.get_master_coordinates(is_b) == (2,0)
        else:
            return self.get_master_coordinates(not(is_b)) == None or self.get_master_coordinates(is_b) == (-2,0)
    def update_is_game_live(self):
        if self.is_win():
            self.is_game_live = False



    def progress_game_state(self,move:move_file.move, should_return = False):
        # update piece coords
        if self.is_b_turn:
            piece = [temp_piece for temp_piece in self.player_b_pieces if temp_piece.coordinates == move.source][0]
        else:
            piece = [temp_piece for temp_piece in self.player_r_pieces if temp_piece.coordinates == move.source][0]
        piece.coordinates = move.target
        # check to see if a piece must be deleted
        if self.is_b_turn:
            self.player_r_pieces = [opposition_piece for opposition_piece in self.player_r_pieces if opposition_piece.coordinates != piece.coordinates]
        else:
            self.player_b_pieces = [opposition_piece for opposition_piece in self.player_b_pieces if opposition_piece.coordinates != piece.coordinates]
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
            piece.future_possible_moves = piece.next_moves(self.player_b_cards)
            for temp_piece in self.player_b_pieces:
                temp_piece.future_possible_moves = temp_piece.add_card(self.player_b_cards[1])
        else:
            piece.future_possible_moves = piece.next_moves(self.player_r_cards) #use thsi for testing func 
            for temp_piece in self.player_r_pieces:
                temp_piece.future_possible_moves = temp_piece.add_card(self.player_r_cards[1])
        # pass play to opposition
        self.is_b_turn = not(self.is_b_turn)
        if should_return:
            return self
        
        
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

def create_game_state(b_pieces,r_pieces,b_cards,r_cards,m_card,is_b):
    return game_state(b_pieces,r_pieces,b_cards,r_cards,m_card,is_b)
def create_random_game_state():
    b_pieces = piece_file.piece.create_pieces(5,[(-2,0),(-2,-2),(-2,-1),(-2,1),(-2,2)],[True,True,True,True,True],[True,False,False,False,False])
    r_pieces = piece_file.piece.create_pieces(5,[(2,0),(2,-2),(2,-1),(2,1),(2,2)],[False,False,False,False,False],[True,False,False,False,False])
    cards = card_file.card.create_5_random_cards()
    g = game_state(b_pieces,r_pieces,[cards[0],cards[1]],[cards[2],cards[3]],cards[4],cards[4].is_stamp_blue) 
    for piece in g.player_b_pieces:
        piece.future_possible_moves = piece.next_moves(g.player_b_cards)#use this to update all cards future possible moves in actual code
    for piece in g.player_r_pieces:
        piece.future_possible_moves = piece.next_moves(g.player_r_cards)
       
    return g