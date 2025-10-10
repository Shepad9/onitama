import numpy as np
import game_state_file
import game_file
import move_file
import gui_file
class player:
    def __init__(self,is_blue): 
        self.is_blue = is_blue
    def get_move(self,state:game_state_file.game_state): 
        source = gui_file.gui_select_square()
        
        if self.is_blue:
            find_piece = [piece for piece in state.player_b_pieces if piece.coordinates == source] # do some error handlig in imput for gui
        else:
            find_piece = [piece for piece in state.player_r_pieces if piece.coordinates == source]
        if len(find_piece) != 1:
            print("no piece")
            return self.get_move(state)
        else:
            piece = find_piece[0]

        gui_file.gui_display(state, source)

        print("source selected")
            
        target = gui_file.gui_select_square()

        print("target selected")

        gui_file.gui_display(state, source, target)
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
        
        potential_move = move_file.move(card,target,piece)  
        if potential_move in state.generate_possible_moves():
            return potential_move
        else:
            print("move not legal")
            return self.get_move(state)




class computer(player):
    def __init__(self, is_blue,depth):
        super().__init__(is_blue)
        self.first_depth = depth

    def static_evaluation(self,state:game_state_file.game_state):
        pass

    def quiescence_search(self,state:game_state_file.game_state):
        pass
        
    def get_move(self, state:game_state_file.game_state, current_line:list[move_file.move], best_line:list[move_file.move], depth = 3,  alpha = -128, beta = 127): #nega max
        if depth == 0:
            return self.quiescence_search(state)
        for potential_move in state.future_possible_moves():
            current_score, best_line = self.get_move(state.progress_game_state(potential_move), current_line.append(potential_move), depth - 1, -alpha, - beta) # recursive call switching alpha and beta for the nega max framework
            if current_score >= beta:
                return beta, best_line #beta cutoff
            if current_score > alpha:
                alpha = current_score # found a new best move
                best_line = current_line
        return alpha, best_line
        


