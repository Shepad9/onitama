import pygame
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


pygame.init()

WIDTH, HEIGHT = 700, 1100
ROWS, COLS = 5, 5
SQUARE_SIZE =  60

window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Onitama game")


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

FONT = pygame.font.SysFont("Comic Sans MS", 30)
save_surface = FONT.render("Save", True, BLACK)
next_file_surface = FONT.render("Next file", True, BLACK)
save_button = pygame.draw.rect(window, WHITE, (0,1000,150,50))

undo_surface = FONT.render("Undo", True, BLACK)
correct_file_surface = FONT.render("Use this file", True, BLACK)
undo_button = pygame.draw.rect(window, WHITE, (150,1000,150,50))

computer_surface = FONT.render("computer players: ", True, BLACK)
computer_blue_marker = pygame.draw.rect(window, WHITE, (150, 150, 150, 50))
computer_red_marker = pygame.draw.rect(window, WHITE, (150, 700, 150, 50))

player_surface = FONT.render("human player", True, BLACK)
player_button_blue = pygame.draw.rect(window, WHITE, (450, 150, 150, 50))
player_button_red = pygame.draw.rect(window, WHITE, (450, 700, 150, 50))

diff1_surface = FONT.render("diificulty level 1", True, BLACK)
diff1_button_blue = pygame.draw.rect(window, WHITE, (150, 300, 150, 50))
diff1_button_red = pygame.draw.rect(window, WHITE, (150, 850, 150, 50))

diff2_surface = FONT.render("diificulty level 2", True, BLACK)
diff2_button_blue = pygame.draw.rect(window, WHITE, (150, 350, 150, 50))
diff2_button_red = pygame.draw.rect(window, WHITE, (150, 900, 150, 50))

diff3_surface = FONT.render("diificulty level 3", True, BLACK)
diff3_button_blue = pygame.draw.rect(window, WHITE, (150, 400, 150, 50))
diff3_button_red = pygame.draw.rect(window, WHITE, (150, 950, 150, 50))

confirm_surface = FONT.render("Confirm", True, BLACK)
confirm_button = pygame.draw.rect(window, WHITE, (550,1000,150,50))

new_game_surface = FONT.render("New game", True, BLACK)
new_game_button = pygame.draw.rect(window, WHITE, (300,150,150,50))

load_game_surface = FONT.render("Load game", True, BLACK)
load_game_button = pygame.draw.rect(window, WHITE, (300,800,150,50))

up_arrow = pygame.transform.scale(
    pygame.image.load("assets/up_arrow.svg"), 
    (SQUARE_SIZE, SQUARE_SIZE*5)
    )
down_arrow = pygame.transform.scale(
    pygame.image.load("assets/down_arrow.svg"), 
    (SQUARE_SIZE, SQUARE_SIZE*5)
    )
right_arrow = pygame.transform.scale(
    pygame.image.load("assets/right_arrow.svg"), 
    (SQUARE_SIZE*5, SQUARE_SIZE)
    )

PIECES_TO_PICTURES = {}

for piece in ["bk", "bp", "wk", "wp"]:
    PIECES_TO_PICTURES[piece] = pygame.transform.scale(
    pygame.image.load(f"assets/{piece}.svg"), 
    (SQUARE_SIZE, SQUARE_SIZE)
    )




def display_card(card_matrix, x , y, position_colour):
    
    for rowi, row in enumerate(card_matrix):
        for coli, item in enumerate(row):
            colour = position_colour if (item == 1) else WHITE
            if (rowi,coli) == (2,2):
                colour = BLACK
            pygame.draw.rect(window, colour, ((coli*SQUARE_SIZE)+x, (rowi*SQUARE_SIZE)+y, SQUARE_SIZE, SQUARE_SIZE))

def game_display(state:game_state_file.game_state, source = None, target = None, is_file_cycling = False):
    if is_file_cycling:
        window.fill(WHITE)
    else:
        if state.is_b_turn:
            window.fill(LIGHT_BLUE)
        else:
            window.fill(LIGHT_RED)
    

    for rowi in range(ROWS):
        for coli in range(COLS):
            colour = WHITE if (rowi + coli) % 2 == 0 else GREY
            pygame.draw.rect(window, colour, ((coli*SQUARE_SIZE)+400, (rowi*SQUARE_SIZE)+350, SQUARE_SIZE, SQUARE_SIZE))
            if (rowi-2,coli-2) == source:
                pygame.draw.rect(window, YELLOW_HIGHLIGHT, ((coli*SQUARE_SIZE)+400, (rowi*SQUARE_SIZE)+350, SQUARE_SIZE, SQUARE_SIZE), 4)
            if (rowi-2,coli-2) == target:
                pygame.draw.rect(window, GREEN_HIGHLIGHT, ((coli*SQUARE_SIZE)+400, (rowi*SQUARE_SIZE)+350, SQUARE_SIZE, SQUARE_SIZE), 4)
            board = get_board(state)
            piece = board[rowi][coli]
            if piece != "..":
                window.blit(PIECES_TO_PICTURES[piece], ((coli*SQUARE_SIZE)+400, (rowi*SQUARE_SIZE)+350))


    display_card(state.player_b_cards[0].get_flattened_matrix(), 0, 0, BLUE) 
    display_card(state.player_b_cards[1].get_flattened_matrix(), 400, 0, BLUE)
    display_card(np.rot90(state.player_r_cards[0].get_flattened_matrix(), 2), 0, 700, RED)
    display_card(np.rot90(state.player_r_cards[1].get_flattened_matrix(), 2), 400, 700, RED)
    display_card(np.rot90(state.middle_card.get_flattened_matrix()), 0, 350, DARK_GREEN)
    if is_file_cycling:
        window.blit(next_file_surface,(save_button.x + 5, save_button.y + 5))
        window.blit(correct_file_surface,(undo_button.x + 5, undo_button.y + 5))
    else:
        window.blit(save_surface,(save_button.x + 5, save_button.y + 5))
        window.blit(undo_surface,(undo_button.x + 5, undo_button.y + 5))
    window.blit(up_arrow, (5, 700))
    window.blit(up_arrow, (400, 700))
    window.blit(down_arrow, (240, 0))
    window.blit(down_arrow, (640, 0))
    window.blit(right_arrow, (0,350))

    
    pygame.display.flip()


def gui_select_square():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if save_button.collidepoint(event.pos):
                    return "save_command"
                if undo_button.collidepoint(event.pos):
                    return "undo_command"
                else:
                    pos = pygame.mouse.get_pos()
                    col = ((pos[0]-400) // SQUARE_SIZE) -2
                    row = ((pos[1]-350) // SQUARE_SIZE) -2
                    return (row, col)
            




 
def get_card(): # returns tuple (-1,-1) didnt click on a card else first number is is_b second number index of card
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
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
                
def get_players(blue = "player", red = "player"):
    window.fill(LIGHT_BLUE)
    pygame.draw.rect(window, LIGHT_RED, (0,550, 700, 550))
    window.blit(computer_surface,(computer_blue_marker.x + 5, computer_blue_marker.y + 5))
    window.blit(computer_surface,(computer_red_marker.x + 5, computer_red_marker.y + 5))
    window.blit(diff1_surface,(diff1_button_blue.x + 5, diff1_button_blue.y + 5))
    window.blit(diff1_surface,(diff1_button_red.x + 5, diff1_button_red.y + 5))
    window.blit(diff2_surface,(diff2_button_blue.x + 5, diff2_button_blue.y + 5))
    window.blit(diff2_surface,(diff2_button_red.x + 5, diff2_button_red.y + 5))
    window.blit(diff3_surface,(diff3_button_blue.x + 5, diff3_button_blue.y + 5))
    window.blit(diff3_surface,(diff3_button_red.x + 5, diff3_button_red.y + 5))
    window.blit(player_surface,(player_button_blue.x + 5, player_button_blue.y + 5))
    window.blit(player_surface,(player_button_red.x + 5, player_button_red.y + 5))
    window.blit(confirm_surface, (confirm_button.x + 5, confirm_button.y + 5))
    if blue == "diff1":
        pygame.draw.rect(window, YELLOW_HIGHLIGHT, (diff1_button_blue.x, diff1_button_blue.y, 150, 50), 4)
    elif blue == "diff2":
        pygame.draw.rect(window, YELLOW_HIGHLIGHT, (diff2_button_blue.x, diff2_button_blue.y, 150, 50), 4)
    elif blue == "diff3":
        pygame.draw.rect(window, YELLOW_HIGHLIGHT, (diff3_button_blue.x, diff3_button_blue.y, 150, 50), 4)
    elif blue == "player":
        pygame.draw.rect(window, YELLOW_HIGHLIGHT, (player_button_blue.x, player_button_blue.y, 150, 50), 4)
    if red == "diff1":
        pygame.draw.rect(window, YELLOW_HIGHLIGHT, (diff1_button_red.x, diff1_button_red.y, 150, 50), 4)
    elif red == "diff2":
        pygame.draw.rect(window, YELLOW_HIGHLIGHT, (diff2_button_red.x, diff2_button_red.y, 150, 50), 4)
    elif red == "diff3":
        pygame.draw.rect(window, YELLOW_HIGHLIGHT, (diff3_button_red.x, diff3_button_red.y, 150, 50), 4)
    elif red == "player":
        pygame.draw.rect(window, YELLOW_HIGHLIGHT, (player_button_red.x, player_button_red.y, 150, 50), 4)
    pygame.display.flip()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if diff1_button_blue.collidepoint(event.pos):
                    return get_players("diff1", red)
                elif diff2_button_blue.collidepoint(event.pos):
                    return get_players("diff2", red)
                elif diff3_button_blue.collidepoint(event.pos):
                    return get_players("diff3", red)
                elif player_button_blue.collidepoint(event.pos):
                    return get_players("player", red)
                elif diff1_button_red.collidepoint(event.pos):
                    return get_players(blue, "diff1")
                elif diff2_button_red.collidepoint(event.pos):
                    return get_players(blue, "diff2")
                elif diff3_button_red.collidepoint(event.pos):
                    return get_players(blue, "diff3")
                elif player_button_red.collidepoint(event.pos):
                    return get_players(blue, "player")
                elif confirm_button.collidepoint(event.pos):
                    return (blue, red)
    
def get_game_file_type(): # returns is new game
    window.fill(GREY)
    window.blit(new_game_surface,(new_game_button.x + 5, new_game_button.y + 5))
    window.blit(load_game_surface,(load_game_button.x + 5, load_game_button.y + 5))
    pygame.display.flip()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if new_game_button.collidepoint(event.pos):
                    return True
                elif load_game_button.collidepoint(event.pos):
                    return False
            
def is_correct_game_file():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if save_button.collidepoint(event.pos):
                    return False
                elif undo_button.collidepoint(event.pos):
                    return True