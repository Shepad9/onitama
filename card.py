import numpy as np
import pandas as pd
class card:
    def __init__(self,name,movement_abilities,is_stamp_blue):
        self.name = name
        self.movement_abilities = movement_abilities
        self.is_stamp_blue = is_stamp_blue

    def create_card(name:str):
        cards = pd.read_csv("/home/shepad/projects/onitama/card.txt",index_col="name")
        return card(name,cards.loc[name][1:27].to_numpy(dtype=np.int16),cards.loc[name][1] == "Blue")
    def display(self):
        print(self.name)
        print(self.is_stamp_blue)
        print(self.movement_abilities.reshape(5,5))

card.create_card("Tiger").display()