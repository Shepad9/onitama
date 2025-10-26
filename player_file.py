import numpy as np
import game_state_file
import move_file
import gui_file
import random
from time import sleep
from copy import deepcopy
from copy import copy
 
GAME_WIN_SCORE = 128
TIME_TO_MOVE = 2 #seconds
SEARCH_DEPTH = 3


class player:
    def __init__(self,is_blue): 
        self.is_blue = is_blue
    def get_move(self,state:game_state_file.game_state): 
        

        source = gui_file.gui_select_square()
        if type(source) == str:
            return source
            

        gui_file.game_display(state, source)

        print("source selected")
            
        target = gui_file.gui_select_square()

        print("target selected")

        gui_file.game_display(state, source, target)
        card_finder = gui_file.get_card()
          
        if self.is_blue and card_finder[0] == 0:
            card = state.player_b_cards[card_finder[1]]
        elif not(self.is_blue) and card_finder[0] == 1:
            card = state.player_r_cards[card_finder[1]]
        elif card_finder == (-1,-1):
            print("not a card")
            return self.get_move(state)
        else:
            print("error has occured")
            return self.get_move(state)
        
        potential_move = move_file.move(card,target,source)  
        if potential_move in state.generate_possible_moves():
            return potential_move
        else:
            print("move not legal")
            return self.get_move(state) 


class full_random(player):
    def __init__(self, is_blue):
        super().__init__(is_blue)

    def get_move(self, state):
        sleep(TIME_TO_MOVE)
        return random.choice(state.generate_possible_moves())


class computer(player):
    
    

    def __init__(self, is_blue, weights = {"total pieces": 10, "piece progression": 1, "master to temple": 2}):
        super().__init__(is_blue)
        self.weights = weights

    def move_ordering_heuristic(self, move:move_file.move, is_b): # lower returns yield high priorities to be checked first
        if is_b:
            return move.source[0] - move.target[0] 
        return move.target[0] - move.source[0]

    def heuristic_move_sorter(self, moves:np.array, is_b):
        heuristic_move_mask = np.argsort(np.array([self.move_ordering_heuristic(move, is_b) for move in moves]))
        return np.take_along_axis(moves, heuristic_move_mask, axis = 0)



    def __total_piece_eval(self, state:game_state_file.game_state): # returns a value from -4 to 4
        return len(state.player_b_pieces) - len(state.player_r_pieces)
    def __piece_progression_eval(self, state:game_state_file.game_state): # return a value from -15 to 15
        return sum([piece.coordinates[0] for piece in state.player_b_pieces]) + sum([piece.coordinates[0] for piece in state.player_r_pieces])
    def __master_to_temple_eval(self, state:game_state_file.game_state): # return a value from -6 to 6
        blue_m, red_m = state.get_master_coordinates(True), state.get_master_coordinates(False)
        return blue_m[0] - abs(blue_m[1]) + red_m[0] + abs(red_m[1])

    def static_evaluation(self, state:game_state_file.game_state): # red is the minimizimg player
        if state.is_game_live == False:
            if state.is_b_turn:
                return GAME_WIN_SCORE
            else:
                return -GAME_WIN_SCORE
        return self.__total_piece_eval(state)*self.weights["total pieces"] + self.__piece_progression_eval(state)*self.weights["piece progression"] + self.__master_to_temple_eval(state)*self.weights["master to temple"]

    def __quiescence_search(self,state:game_state_file.game_state):
        pass

    def maximiser(
            self, 
            state:game_state_file.game_state, 
            depth = SEARCH_DEPTH,  
            best_line:list[move_file.move] = [],  
            alpha = -GAME_WIN_SCORE -1, 
            beta = GAME_WIN_SCORE + 1
        ): 
        # always return dict (score, asc line, best line)
        if depth == 0 or state.is_win():
            return {"score":self.static_evaluation(state), "asc_line":[],"best_line": best_line} # return dict
        all_moves = self.heuristic_move_sorter(state.generate_possible_moves(), state.is_b_turn)
        for potential_move in all_moves:
            working_state = deepcopy(state) # prevents errors caused by python passing references rather than values
            working_state.progress_game_state(potential_move)
            ret = self.minimiser(
                working_state, 
                depth - 1, 
                best_line, 
                alpha, 
                beta
            )
            current_score, asc_current_line = ret["score"] , ret["asc_line"] + [potential_move]
             # recursive call 
            if current_score >= beta: # beta cutoff
                return {"score":beta, "asc_line":asc_current_line,"best_line": best_line} #beta cutoff
            if current_score > alpha: # found a new best move
                alpha = current_score
                best_line = asc_current_line
                
                
        return {"score":alpha, "asc_line":asc_current_line,"best_line": best_line}
                
        

    
    def minimiser(
            self, 
            state:game_state_file.game_state, 
            depth = SEARCH_DEPTH,  
            best_line:list[move_file.move] = [],  
            alpha = -GAME_WIN_SCORE -1, 
            beta = GAME_WIN_SCORE + 1
        ): 
        # always return tuple (score, asc line, best line)
        if depth == 0 or state.is_win():
            return {"score":self.static_evaluation(state), "asc_line":[],"best_line": best_line} # return dict
        all_moves = self.heuristic_move_sorter(state.generate_possible_moves(), state.is_b_turn)
        for potential_move in all_moves:
            working_state = deepcopy(state) # prevents errors caused by python passing references rather than values
            working_state.progress_game_state(potential_move)
            ret = self.maximiser(
                working_state, 
                depth - 1, 
                best_line, 
                alpha,
                beta
            )
            current_score, asc_current_line = ret["score"], ret["asc_line"] + [potential_move]
             # recursive call switching alpha and beta for the nega max framework
            if current_score <= alpha: # alpha cutoff
                return {"score":alpha, "asc_line":asc_current_line,"best_line": best_line} #beta cutoff
            if current_score < beta: # found a new best move
                beta = current_score
                best_line = asc_current_line
                
                
        return {"score":beta, "asc_line":asc_current_line,"best_line": best_line}
    
        
    def get_move(self, state:game_state_file.game_state):
        
        #sleep(TIME_TO_MOVE)
        if state.is_b_turn:
            ret = self.maximiser(state)
        else:
            ret = self.minimiser(state)
        print(ret["score"])
        move = ret["best_line"][-1]
        return move_file.move(move.card ,tuple([int(x) for x in move.target]), move.source)
        
    
        


