#---------player_file.py----------

import numpy as np
import game_state_file
import move_file
import gui_file
import random
from time import sleep
from copy import deepcopy
from copy import copy
 
GAME_WIN_SCORE = 1023
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

        
            
        target = gui_file.gui_select_square()

       

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
        #sleep(TIME_TO_MOVE)
        return random.choice(state.generate_possible_moves())


class computer(player):
    
    

    def __init__(self, is_blue, weights = {"total pieces": (10, 15), "piece progression": (1, 0), "master to temple": (0, 5), "defended pieces": (3, 1), "attacked squares": (2,3)}, noise = 0):
        super().__init__(is_blue)
        self.weights = weights
        self.noise = noise

    def all_accesible_squares(self, state:game_state_file.game_state, is_b = None):
        if is_b == None or is_b == state.is_b_turn:
            moves = state.generate_possible_moves(True)
            return set([move.target for move in moves])
        moves = state.generate_possible_moves(False)
        return set([move.target for move in moves])
    
    def master_accesible_squares(self, state:game_state_file.game_state, is_b = None):
        if is_b == None or is_b == state.is_b_turn:
            moves = state.generate_possible_moves(True)
            return set([move.target for move in moves if move.source == state.get_master_coordinates(True)])
        moves = state.generate_possible_moves(False)
        return set([move.target for move in moves if move.source == state.get_master_coordinates(False)])
        
    
    def __get_b_piece_coords(self,state:game_state_file.game_state):
        return [piece.coordinates for piece in state.player_b_pieces]
    
    def __get_r_piece_coords(self,state:game_state_file.game_state):
        return [piece.coordinates for piece in state.player_r_pieces]


    def is_quiet(self, state:game_state_file.game_state): # quiet means game cannot be won on the next turn
        master_targets = self.master_accesible_squares(state)
        if state.is_b_turn == True and (state.get_master_coordinates(False) in master_targets or (2,0) in master_targets):
            return False
        if state.is_b_turn == False and (state.get_master_coordinates(True) in master_targets or (-2,0) in master_targets):
            return False
        return True
    
    def which_weighting(self, state:game_state_file.game_state): 
        if len(state.player_b_pieces) + len(state.player_r_pieces) > 6:
            return 0
        return 1

    def quiescence_max(self, state:game_state_file.game_state, best_score = -GAME_WIN_SCORE):
        if self.is_quiet(state):
            return self.static_evaluation(state)
        moves = state.generate_possible_moves()
        for potential_move in moves:
            working_state = deepcopy(state) # prevents errors caused by python passing references rather than values
            working_state.progress_game_state(potential_move)
            score = self.quiescence_min(working_state, best_score)
            if score == None:
                raise Exception("why is score none")
            if score > best_score:
                best_score = score
            return best_score

    def quiescence_min(self, state:game_state_file.game_state, best_score = GAME_WIN_SCORE):
        if self.is_quiet(state):
            return self.static_evaluation(state)
        moves = state.generate_possible_moves()
        for potential_move in moves:
            working_state = deepcopy(state) # prevents errors caused by python passing references rather than values
            working_state.progress_game_state(potential_move)
            score = self.quiescence_max(working_state, best_score)
            if score < best_score:
                best_score = score
            return best_score

    def move_ordering_heuristic(self, move:move_file.move, is_b): # higher returns yield high priorities to be checked first
        if is_b:
            return move.source[0] - move.target[0] 
        return move.target[0] - move.source[0]

    def heuristic_move_sorter(self, moves:np.array, is_b):
        heuristic_move_mask = np.argsort(np.array([self.move_ordering_heuristic(move, is_b) for move in moves]))
        return np.take_along_axis(moves, heuristic_move_mask, axis = 0)


    def __defended_pieces_eval(self, state:game_state_file.game_state): #pieces cannot be defended multiple times return a value from roughly 10 to - 10
        blue_possible_targets = self.all_accesible_squares(state, True)
        defended_blue = len([location for location in blue_possible_targets if location in self.__get_b_piece_coords(state)])
        red_possible_targets = self.all_accesible_squares(state, False)
        defended_red = len([location for location in red_possible_targets if location in self.__get_r_piece_coords(state)])
        return defended_blue - defended_red
    
    def __attacked_squares_eval(self, state:game_state_file.game_state): #returns a value from roughly 25 to - 25
        blue_possible_targets = self.all_accesible_squares(state, True)
        red_possible_targets = self.all_accesible_squares(state, False)
        return len(blue_possible_targets) - len(red_possible_targets)

        
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
        w = self.which_weighting(state) # below line sums all the heuristics with a weighting
        return self.__total_piece_eval(state)*self.weights["total pieces"][w] + self.__piece_progression_eval(state)*self.weights["piece progression"][w] + self.__master_to_temple_eval(state)*self.weights["master to temple"][w] + self.__defended_pieces_eval(state)*self.weights["defended pieces"][w] + self.__attacked_squares_eval(state)*self.weights["attacked squares"][w] +random.randint(-5,5) * self.noise


    def maximiser(
            self, 
            state:game_state_file.game_state, 
            depth = SEARCH_DEPTH,  
            best_line:list[move_file.move] = [],  
            alpha = -GAME_WIN_SCORE -1, 
            beta = GAME_WIN_SCORE + 1
        ): 
        # always return dict (score, asc line, best line)
        if depth == 0:
            return {"score":self.quiescence_max(state), "asc_line":[],"best_line": best_line} # return dict
        if state.is_win():
            return {"score":self.static_evaluation(state), "asc_line":[],"best_line": best_line}
        

        all_moves = self.heuristic_move_sorter(state.generate_possible_moves(), state.is_b_turn)

        if len(all_moves) == 0:
            return {"score":self.static_evaluation(state), "asc_line":[],"best_line": best_line}
        
        for potential_move in all_moves:
            working_state = deepcopy(state) # prevents errors caused by python passing references rather than values
            working_state.progress_game_state(potential_move)
            # does something... probably?
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
                
                
        return {"score":alpha, "asc_line":asc_current_line,"best_line": 
                best_line}
                
        

    
    def minimiser(
            self, 
            state:game_state_file.game_state, depth = SEARCH_DEPTH,  
            best_line:list[move_file.move] = [],  
            alpha = -GAME_WIN_SCORE -1, 
            beta = GAME_WIN_SCORE + 1
        ): 
        # always return tuple (score, asc line, best line)
        if depth == 0:
            return {"score":self.quiescence_min(state), "asc_line":[],"best_line": best_line} # return dict
        if state.is_win():
            return {"score":self.static_evaluation(state), "asc_line":[],"best_line": best_line}
        
        all_moves = self.heuristic_move_sorter(state.generate_possible_moves(), state.is_b_turn)

        if len(all_moves) == 0:
            return {"score":self.static_evaluation(state), "asc_line":[],"best_line": best_line}
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
        
        move = ret["best_line"][-1]
        return move_file.move(move.card ,tuple([int(x) for x in move.target]), move.source)
        
    

