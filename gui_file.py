import pygame as pg
import sys
import numpy as np
import game_state_file
import piece_file
import card_file


def get_board(state:game_state_file.game_state):
    board = np.reshape(np.array([".."]*25),(5,5))
    for piece in state.player_b_pieces:
        if piece.is_master == True:
            board[piece.coordinates[0]+2][piece.coordinates[1]+2] = "bk" #blue master
        else:
            board[piece.coordinates[0]+2][piece.coordinates[1]+2] = "bp" #blue pawn
    for piece in state.player_r_pieces:
        if piece.is_master == True:
            board[piece.coordinates[0]+2][piece.coordinates[1]+2] = "wk" #red master
        else:
            board[piece.coordinates[0]+2][piece.coordinates[1]+2] = "wp" #red pawn
    return board


pg.init()


WIDTH, HEIGHT = 700, 1000
ROWS, COLS = 5, 5
SQUARE_SIZE =  60

GREY = (88, 94, 99)
WHITE = (255, 255, 255)
GREEN = (118, 150, 86)
BLACK = (0,0,0)
RED = (209, 0, 0)
BLUE = (26, 96, 232)
DARK_GREEN = (13, 158, 61)
LIGHT_BLUE = (119, 204, 241)
LIGHT_RED = (234, 80, 80)
YELLOW_HIGHLIGHT = (255, 228, 0)
GREEN_HIGHLIGHT = (0, 255, 4)


up_arrow = pg.transform.scale(
    pg.image.load("assets/up_arrow.svg"), 
    (SQUARE_SIZE, SQUARE_SIZE*5)
    )
down_arrow = pg.transform.scale(
    pg.image.load("assets/down_arrow.svg"), 
    (SQUARE_SIZE, SQUARE_SIZE*5)
    )
right_arrow = pg.transform.scale(
    pg.image.load("assets/right_arrow.svg"), 
    (SQUARE_SIZE*5, SQUARE_SIZE)
    )

PIECES_TO_PICTURES = {}

for piece in ["bk", "bp", "wk", "wp"]:
    PIECES_TO_PICTURES[piece] = pg.transform.scale(
    pg.image.load(f"assets/{piece}.svg"), 
    (SQUARE_SIZE, SQUARE_SIZE)
    )
window = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Onitama game")

def display_card(card_matrix, x , y, position_colour):
    
    for rowi, row in enumerate(card_matrix):
        for coli, item in enumerate(row):
            colour = position_colour if (item == 1) else WHITE
            if (rowi,coli) == (2,2):
                colour = BLACK
            pg.draw.rect(window, colour, ((coli*SQUARE_SIZE)+x, (rowi*SQUARE_SIZE)+y, SQUARE_SIZE, SQUARE_SIZE))

def gui_display(state:game_state_file.game_state, source = None, target = None):
    
    if state.is_b_turn:
        window.fill(LIGHT_BLUE)
    else:
        window.fill(LIGHT_RED)
    

    for rowi in range(ROWS):
        for coli in range(COLS):
            colour = WHITE if (rowi + coli) % 2 == 0 else GREY
            pg.draw.rect(window, colour, ((coli*SQUARE_SIZE)+400, (rowi*SQUARE_SIZE)+350, SQUARE_SIZE, SQUARE_SIZE))
            if (rowi-2,coli-2) == source:
                pg.draw.rect(window, YELLOW_HIGHLIGHT, ((coli*SQUARE_SIZE)+400, (rowi*SQUARE_SIZE)+350, SQUARE_SIZE, SQUARE_SIZE), 4)
            if (rowi-2,coli-2) == target:
                pg.draw.rect(window, GREEN_HIGHLIGHT, ((coli*SQUARE_SIZE)+400, (rowi*SQUARE_SIZE)+350, SQUARE_SIZE, SQUARE_SIZE), 4)
            board = get_board(state)
            piece = board[rowi][coli]
            if piece != "..":
                window.blit(PIECES_TO_PICTURES[piece], ((coli*SQUARE_SIZE)+400, (rowi*SQUARE_SIZE)+350))


    display_card(state.player_b_cards[0].get_flattened_matrix(), 0, 0, BLUE) 
    display_card(state.player_b_cards[1].get_flattened_matrix(), 400, 0, BLUE)
    display_card(np.rot90(state.player_r_cards[0].get_flattened_matrix(), 2), 0, 700, RED)
    display_card(np.rot90(state.player_r_cards[1].get_flattened_matrix(), 2), 400, 700, RED)
    display_card(np.rot90(state.middle_card.get_flattened_matrix()), 0, 350, DARK_GREEN)
    window.blit(up_arrow, (5, 700))
    window.blit(up_arrow, (400, 700))
    window.blit(down_arrow, (240, 0))
    window.blit(down_arrow, (640, 0))
    window.blit(right_arrow, (0,350))

    
    pg.display.flip()



def gui_select_square():
    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

            if event.type == pg.MOUSEBUTTONDOWN:
                pos = pg.mouse.get_pos()
                col = ((pos[0]-400) // SQUARE_SIZE) -2
                row = ((pos[1]-350) // SQUARE_SIZE) -2
                return (row, col)




 
def get_card(): # returns tuple (-1,-1) didnt click on a card else first number is is_b second number index of card
    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

            if event.type == pg.MOUSEBUTTONDOWN:
                pos = pg.mouse.get_pos()
                if pos[0] < 300 and pos[1] < 300:
                    return (0,0)
                elif pos[0] > 400 and pos[1] < 300:
                    return (0,1)
                elif pos[0] < 300 and pos[1] > 700:
                    return (1,0)
                elif pos[0] > 400 and pos[1] > 700:
                    return (1,1)
                else:
                    return (-1,-1)