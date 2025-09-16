import card
import move
import numpy as np
class piece_obj:
    def __init__(self, coordinates:tuple, is_blue:bool, is_master:bool, future_possible_moves = np.array([0])):
        self.coordinates = coordinates
        self.is_blue = is_blue
        self.is_master = is_master
        self.future_possible_moves = future_possible_moves
    def update_future_possible_moves(self,card_obj):
        if self.is_blue : #blue playing down the board
            self.future_possible_moves = np.array([
                move.move_obj(card_obj,self.coordinates,(self.coordinates[0] + delta[0], self.coordinates[1] + delta[1]))
                for delta in card_obj.movement_abilities
                if (
                    (delta[0] + self.coordinates[0] < 3) and
                    (delta[1] + self.coordinates[1] < 3) and
                    (delta[0] + self.coordinates[0] > -3) and
                    (delta[1] + self.coordinates[1] > -3)
                    )
                ])
        else: # red playing up the board
             self.future_possible_moves = np.array([
                move.move_obj(card_obj,self.coordinates,(self.coordinates[0] - delta[0], self.coordinates[1] - delta[1]))
                for delta in card_obj.movement_abilities
                if (
                    (delta[0] - self.coordinates[0] < 3) and
                    (delta[1] - self.coordinates[1] < 3) and
                    (delta[0] - self.coordinates[0] > -3) and
                    (delta[1] - self.coordinates[1] > -3)
                    )
                ])

       
        
