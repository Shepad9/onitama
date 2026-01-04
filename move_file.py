#--------main_file.py----------

import numpy as np
class move:
    def __init__(self,card,target, source):
        self.card = card
        self.target = target
        self.source = source

        
    def __eq__(self, other):
        return self.card == other.card and list(self.target) == list(other.target) and list(self.source) == list(other.source)
    
   

