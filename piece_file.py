import card_file
import move_file
import numpy as np
class piece:
    def __init__(self, coordinates:tuple, is_blue:bool, is_master:bool, future_possible_moves = np.array([0])):
        self.coordinates = coordinates
        self.is_blue = is_blue
        self.is_master = is_master
        self.future_possible_moves = future_possible_moves

    def create_pieces(n,coordinates,is_b,is_m):
        lst = []
        for i in range(n):
            current_piece = piece(coordinates[i],is_b[i],is_m[i])
        
            lst.append(current_piece)

        return lst
    
    def update_future_possible_moves(self,card):  # returns the future possible moves for 1 card and 1 piece
        if self.is_blue : #blue playing down the board
            return  np.array([
                move_file.move(card,(self.coordinates[0] + delta[0], self.coordinates[1] + delta[1]), self)
                for delta in card.movement_abilities
                if (
                    (delta[0] + self.coordinates[0] < 3) and
                    (delta[1] + self.coordinates[1] < 3) and
                    (delta[0] + self.coordinates[0] > -3) and
                    (delta[1] + self.coordinates[1] > -3)
                    )
                ])
        else: # red playing up the board
             return  np.array([
                move_file.move(card,(self.coordinates[0] - delta[0], self.coordinates[1] - delta[1]), self)
                for delta in card.movement_abilities
                if (
                    (delta[0] - self.coordinates[0] < 3) and
                    (delta[1] - self.coordinates[1] < 3) and
                    (delta[0] - self.coordinates[0] > -3) and
                    (delta[1] - self.coordinates[1] > -3)
                    )
                ])
        
    def add_card(self,card):#adds the future possible moves of a new card after a move and a new card is accesible
        return  np.concatenate((self.future_possible_moves, self.update_future_possible_moves(card)))
        

             
    def next_moves(self,cards): # returns all future possible moves for the piece with both cards
        return  np.concatenate((self.update_future_possible_moves(cards[0]), self.update_future_possible_moves(cards[1])))
        

    def is_clash(self,potential_move): #checks whwther the move is blocked by a allied piece
        return  potential_move.target == self.coordinates

       
        
