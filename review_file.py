#----------review_file.py---------

import gui_file
import game_state_file
import move_file
import player_file
from copy import deepcopy

class review:
    def __init__(self, initial_game_state:game_state_file.game_state, move_stack:list[move_file.move], move_item_index = 0):
        self.current_game_state = deepcopy(initial_game_state)
        self.initial_game_state = initial_game_state
        self.move_stack = move_stack
        self.move_index = move_item_index
        gui_file.game_display(initial_game_state, is_review=True)
    
    def progress(self):
        if self.move_index < len(self.move_stack):
            self.current_game_state.progress_game_state(self.move_stack[self.move_index])
            self.move_index += 1
            gui_file.game_display(self.current_game_state, is_review=True)
    def regress(self):
        if self.move_index > 0:
            self.current_game_state = deepcopy(self.initial_game_state)
            self.move_index -= 1
            for move in self.move_stack[:self.move_index]:
                self.current_game_state.progress_game_state(move)
            gui_file.game_display(self.current_game_state, is_review=True)
    def reveal_move(self):
        com = player_file.computer(self.current_game_state.is_b_turn)
        hint_move = com.get_move(self.current_game_state)
        gui_file.game_display(self.current_game_state, hint_source=hint_move.source, hint_target= hint_move.target, is_review=True)
    
    

    def review(self):
        quit = False
        while not(quit):
            command = gui_file.review_command()
            if command == "quit":
                quit = True
            if command == "progress":
                self.progress()
            if command == "undo":
                self.regress()
            if command == "move":
                self.reveal_move()


        