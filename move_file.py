import numpy as np
class move:
    def __init__(self,card,target,piece):
        self.card = card
        self.target = target
        self.piece = piece
    def __eq__(self, other):
        return self.card == other.card and list(self.target) == list(other.target) and self.piece == other.piece
        