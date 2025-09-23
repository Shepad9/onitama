import card_file
import move_file
import numpy as np
class piece:
    def __init__(self, coordinates:tuple, is_blue:bool, is_master:bool, future_possible_moves = np.array([0])):
        self.coordinates = coordinates
        self.is_blue = is_blue
        self.is_master = is_master
        self.future_possible_moves = future_possible_moves
    def update_future_possible_moves(self,card):
        if self.is_blue : #blue playing down the board
            return  np.array([
                move_file.move(card,self.coordinates,(self.coordinates[0] + delta[0], self.coordinates[1] + delta[1]), self)
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
                move_file.move(card,self.coordinates,(self.coordinates[0] - delta[0], self.coordinates[1] - delta[1]), self)
                for delta in card.movement_abilities
                if (
                    (delta[0] - self.coordinates[0] < 3) and
                    (delta[1] - self.coordinates[1] < 3) and
                    (delta[0] - self.coordinates[0] > -3) and
                    (delta[1] - self.coordinates[1] > -3)
                    )
                ])
             
    def next_moves(self,cards): # returns all future possible moves for the piece with both cards
        self.future_possible_moves = np.concatenate((self.update_future_possible_moves(cards[0]), self.update_future_possible_moves(cards[1])))

    def is_clash(self,potential_move): #checks whwther the move is blocked by a allied piece
        return  potential_move.target == self.coordinates
       
        
