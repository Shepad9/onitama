import numpy as np
import pandas as pd
class card:
    def __init__(self,name,movement_abilities,is_stamp_blue):
        self.name = name
        self.movement_abilities = np.argwhere(np.reshape(movement_abilities,(5,5))==True)
        self.is_stamp_blue = is_stamp_blue

    def create_card(name:str):
        cards = pd.read_csv("/home/shepad/projects/onitama/card.txt",index_col="name")
        return card(name,cards.loc[name][1:27].to_numpy(dtype=bool),cards.loc[name][1] == "Blue")
    
    def get_flattened_matrix(self)->np.array:
        mat = np.zeros((5,5))
        for delta in self.movement_abilities:
            mat[delta[0],delta[1]] = 1
        return mat
    def display(self):
        print(self.name)
        print(self.is_stamp_blue)
        print(np.reshape(self.get_flattened_matrix(),(5,5)))
        
(card.create_card("Tiger")).display()
