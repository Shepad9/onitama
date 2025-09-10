import card
class piece:
    def __init__(self, coordinates, is_blue:bool, is_master:bool, future_possible_moves):
        self.coordinates = coordinates
        self.is_blue = is_blue
        self.is_master = is_master
        self.future_possible_moves = future_possible_moves
    def generate_future_possible_moves(self,card):
        pass # add this funtion takes card as input and outputs a move object also update docs