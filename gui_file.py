#---------gui_file.py---------

import pygame
import sys
import numpy as np
from pathlib import Path

import game_state_file

BASE_PATH = Path(__file__).resolve().parent


def get_board(state:game_state_file.game_state):
    board = np.reshape(np.array([".."]*25),(5,5))
    for piece in state.player_b_pieces:
        if piece.is_master == True:
            print(piece.coordinates[0], piece.coordinates[1])
            board[piece.coordinates[0]+2, piece.coordinates[1]+2] = "bk" #blue master
        else:
            board[piece.coordinates[0]+2, piece.coordinates[1]+2] = "bp" #blue pawn
    for piece in state.player_r_pieces:
        if piece.is_master == True:
            board[piece.coordinates[0]+2, piece.coordinates[1]+2] = "wk" #red master
        else:
            board[piece.coordinates[0]+2, piece.coordinates[1]+2] = "wp" #red pawn
    return board


pygame.init()

WIDTH, HEIGHT = 700, 1100
ROWS, COLS = 5, 5
SQUARE_SIZE =  60
SCREEN_SCALE_X = 0.4
SCREEN_SCALE_Y = 0.8

display_info = pygame.display.Info()
WINDOW_WIDTH = int(display_info.current_w * SCREEN_SCALE_X)
WINDOW_HEIGHT = int(display_info.current_h * SCREEN_SCALE_Y)

# Create the window
display_window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Onitama game")

scale_x = WIDTH / WINDOW_WIDTH
scale_y = HEIGHT / WINDOW_HEIGHT

window = pygame.Surface((WIDTH, HEIGHT))



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
YELLOW_HINT = (230, 217, 129)
GREEN_HINT = (139, 172, 58)

FONT = pygame.font.SysFont("Comic Sans MS", 30)
progress_surface = FONT.render("progress", True, BLACK)
quit_surface = FONT.render("quit", True, BLACK)

save_surface = FONT.render("Save", True, BLACK)
next_file_surface = FONT.render("Next file", True, BLACK)
save_button = pygame.draw.rect(window, WHITE, (0,1000,150,50))

undo_surface = FONT.render("Undo", True, BLACK)
correct_file_surface = FONT.render("Use this file", True, BLACK)
undo_button = pygame.draw.rect(window, WHITE, (150,1000,150,50))

hint_surface = FONT.render("Hint", True, BLACK)
hint_button = pygame.draw.rect(window, WHITE, (300,1000,150,50))

move_surface = FONT.render("Move", True, BLACK)
move_button = pygame.draw.rect(window, WHITE, (450,1000,100,50)) # 100 because was clashing with instructions

review_surface = FONT.render("review", True, BLACK)

instructions_surface = FONT.render("instructions", True, BLACK)
instructions_button = pygame.draw.rect(window, WHITE, (550,1000,150,50))

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

instructions_text = """
When finished reading press the space bar and scroll in either diretion to return to your game.
buttons at the bottom of the screen are called utility buttons, these are only callable if it the turn of a human player.
Whose turn it is is indicated by the background colour, being either red, or blue, if the background is white you are in the file selection screen which will be displayed below.
to initiate a game select the the players for both colours, if selecting a computer player click on the difficuly, when happy with ur choices click confirm.
Now decide whether you would like a new game or a saved file(some files have been saved for you), if selecting a file you can cycle through all saved files until at the file you wish to load.
Now that you are playing the game, on each turn you must select; the piece you wish to move, the square you wish to move to and the card you wish to use in that order(select each component by clicking on it).
the piece about to move is indicated with a yellow highlight, and the square you are about to move to is indicated with a green highlight.
if you have made a mistake, simply click the piece you wish to move again until it is highlighted in yellow, then continue as normal.
If playing  computer this may take a couple seconds to move, this is normal.
After a game, you have the choice to review, this will allow you to click through the game at your own pace at any point you may ask the computer what it would have played.
the utility buttons are generally intuitive, but know that hint offers you only the piece to move in a different yellow highlight, whilst move tells you where to move the piece aswell in a green highlight.
Note these highlights are just suggestions and you are at liberty to move as normal.
you are also able to watch two computer play eachother, the reccomended way of doing this is letting them play and then reviewing the game.
If unaware as to the rules of Onitama, the game can be won by capturing the opponents master or getting your own master to the opponents temple(where their master starts).
all pieces move according the cards, the movements available to you will be highlighted in your colour, all cards movements are relative to the black square in the middle.
after each move the card used is put in the middle and you gain the middle card for your next turn, the cards rotate this is made somewhat clear via the arrows.
capturing rules are chess like, as in you cannot capture your own pieces and capturing occurs by landing on an opponets piece.
Note: you may move yourself into check and there is no warning given when you are in check.
"""

up_arrow = pygame.transform.scale(
    pygame.image.load(f"{BASE_PATH}/assets/up_arrow.svg"), 
    (SQUARE_SIZE, SQUARE_SIZE*5)
    )
down_arrow = pygame.transform.scale(
    pygame.image.load(f"{BASE_PATH}/assets/down_arrow.svg"), 
    (SQUARE_SIZE, SQUARE_SIZE*5)
    )
right_arrow = pygame.transform.scale(
    pygame.image.load(f"{BASE_PATH}/assets/right_arrow.svg"), 
    (SQUARE_SIZE*5, SQUARE_SIZE)
    )

PIECES_TO_PICTURES = {}

for piece in ["bk", "bp", "wk", "wp"]:
    PIECES_TO_PICTURES[piece] = pygame.transform.scale(
    pygame.image.load(f"{BASE_PATH}/assets/{piece}.svg"), 
    (SQUARE_SIZE, SQUARE_SIZE)
    )


def scaled_display():
    scaled_surface = pygame.transform.smoothscale(window, (WINDOW_WIDTH, WINDOW_HEIGHT))
    display_window.blit(scaled_surface, (0, 0))

    pygame.display.flip()


def should_review(winner:bool):
    if not(winner):
        window.fill(LIGHT_BLUE)
    else:
        window.fill(LIGHT_RED)
    window.blit(review_surface,(new_game_button.x + 5, new_game_button.y + 5))
    window.blit(new_game_surface,(load_game_button.x + 5, load_game_button.y + 5))
    scaled_display()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                x, y = x*scale_x, y*scale_y
                if new_game_button.collidepoint((x,y)):
                    return True
                elif load_game_button.collidepoint((x,y)):
                    return False
                

def display_card(card_matrix, x , y, position_colour):
    
    for rowi, row in enumerate(card_matrix):
        for coli, item in enumerate(row):
            colour = position_colour if (item == 1) else WHITE
            if (rowi,coli) == (2,2):
                colour = BLACK
            pygame.draw.rect(window, colour, ((coli*SQUARE_SIZE)+x, (rowi*SQUARE_SIZE)+y, SQUARE_SIZE, SQUARE_SIZE))


def game_display(
        state:game_state_file.game_state,
        source = None,
        target = None,
        hint_source = None,
        hint_target = None,
        is_file_cycling = False,
        is_review = False
    ):
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
            elif (rowi-2,coli-2) == target:
                pygame.draw.rect(window, GREEN_HIGHLIGHT, ((coli*SQUARE_SIZE)+400, (rowi*SQUARE_SIZE)+350, SQUARE_SIZE, SQUARE_SIZE), 4)
            elif (rowi-2,coli-2) == hint_source:
                pygame.draw.rect(window, YELLOW_HINT, ((coli*SQUARE_SIZE)+400, (rowi*SQUARE_SIZE)+350, SQUARE_SIZE, SQUARE_SIZE), 4)
            elif (rowi-2,coli-2) == hint_target:
                pygame.draw.rect(window, GREEN_HINT, ((coli*SQUARE_SIZE)+400, (rowi*SQUARE_SIZE)+350, SQUARE_SIZE, SQUARE_SIZE), 4)
        
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
    elif is_review:
        window.blit(progress_surface,(save_button.x + 5, save_button.y + 5))
        window.blit(undo_surface,(undo_button.x + 5, undo_button.y + 5))
        window.blit(quit_surface,(hint_button.x + 5, hint_button.y + 5))
        window.blit(move_surface,(move_button.x + 5, move_button.y + 5))
    else:
        window.blit(save_surface,(save_button.x + 5, save_button.y + 5))
        window.blit(undo_surface,(undo_button.x + 5, undo_button.y + 5))
        window.blit(hint_surface,(hint_button.x + 5, hint_button.y + 5))
        window.blit(move_surface,(move_button.x + 5, move_button.y + 5))
        window.blit(instructions_surface,(instructions_button.x + 5, instructions_button.y + 5))

    window.blit(up_arrow, (5, 700))
    window.blit(up_arrow, (400, 700))
    window.blit(down_arrow, (240, 0))
    window.blit(down_arrow, (640, 0))
    window.blit(right_arrow, (0,350))

    scaled_display()


def text_wrapper(text, width_max, font): #written like a greedy algorithm (rare serious code for this file) for instructions thing
    words = text.split(" ")

    lines = []
    current_line = ""
    for word in words:
        potential_line = current_line + word + " "
        if font.size(potential_line)[0] <= width_max:
            current_line = potential_line
        else:
            lines.append(current_line)
            current_line = word + " "
    lines.append(current_line) # bc last line needs to be included
    return lines


def clamp_scroll(scroll, height): # ensures dont scroll of page 30 is the vertical padding
    content_total = height + 30 * 2
    max_scroll = 30  # fully scrolled to top
    min_scroll = min(30, HEIGHT - content_total + 30)

        # If text fits, lock in place
    if content_total <= HEIGHT:
        return 30 # if dont need to scroll lock in position

    return  max(min_scroll, min(max_scroll, scroll)) # return the same unless outside valid range

    
def instructions_display():
    lines = text_wrapper(instructions_text, WIDTH-30, FONT)
    scroll_ofset = 0
    scroll_ofset = clamp_scroll(HEIGHT, scroll_ofset) # line makes scroll_ofset valid repaeated below
    clock = pygame.time.Clock()

    line_height = FONT.get_height() + 3 #dont combine lines we need line height to print lines at bottom
    text_height = len(lines) * line_height

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                       
            if event.type == pygame.MOUSEWHEEL: # wheel scroll
                scroll_ofset += event.y * 30
                scroll_ofset = clamp_scroll(HEIGHT, scroll_ofset)
     
            if event.type == pygame.KEYDOWN: # button scroll
                if event.key == pygame.K_DOWN:
                    scroll_ofset -= 20
                    scroll_ofset = clamp_scroll(HEIGHT, scroll_ofset)
                if event.key == pygame.K_UP:
                    scroll_ofset += 20
                    scroll_ofset = clamp_scroll(HEIGHT, scroll_ofset)
                if event.key == pygame.K_SPACE:
                    return None # leave the intructions page
         
        window.fill(GREY)

        y = 30 + scroll_ofset # 30 is space at the top of the screen
        for line in lines:
            text_surface = FONT.render(line, True, BLACK)
            window.blit(text_surface, (15, y)) #15 is space to left, probably should be a global 
            y += line_height

        scaled_display()
        clock.tick(30)


def gui_select_square():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                x, y = x*scale_x, y*scale_y
                if save_button.collidepoint((x,y)):
                    return "save_command"
                if undo_button.collidepoint((x,y)):
                    return "undo_command"
                if hint_button.collidepoint((x,y)):
                    return "hint_command"
                if move_button.collidepoint((x,y)):
                    return "move_command"
                if instructions_button.collidepoint((x,y)):
                    return "instructions_command"
                else:
                    pos = pygame.mouse.get_pos()
                    col = int(((pos[0] * scale_x)-400) // SQUARE_SIZE) -2
                    row = int(((pos[1] * scale_y)-350) // SQUARE_SIZE) -2
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
                x, y = pos
                x, y = x*scale_x, y*scale_y
                if x < 300 and y < 300:
                    return (0,0)
                elif x > 400 and y < 300:
                    return (0,1)
                elif x < 300 and y > 700:
                    return (1,0)
                elif x > 400 and y > 700:
                    return (1,1)
                else:
                    return (-1,-1)


def show_instructions():
    pass


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
    scaled_display()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                x, y = x*scale_x, y*scale_y
                if diff1_button_blue.collidepoint((x,y)):
                    return get_players("diff1", red)
                elif diff2_button_blue.collidepoint((x,y)):
                    return get_players("diff2", red)
                elif diff3_button_blue.collidepoint((x,y)):
                    return get_players("diff3", red)
                elif player_button_blue.collidepoint((x,y)):
                    return get_players("player", red)
                elif diff1_button_red.collidepoint((x,y)):
                    return get_players(blue, "diff1")
                elif diff2_button_red.collidepoint((x,y)):
                    return get_players(blue, "diff2")
                elif diff3_button_red.collidepoint((x,y)):
                    return get_players(blue, "diff3")
                elif player_button_red.collidepoint((x,y)):
                    return get_players(blue, "player")
                elif confirm_button.collidepoint((x,y)):
                    return (blue, red)
                
    
def get_game_file_type(): # returns is new game
    window.fill(GREY)
    window.blit(new_game_surface,(new_game_button.x + 5, new_game_button.y + 5))
    window.blit(load_game_surface,(load_game_button.x + 5, load_game_button.y + 5))
    scaled_display()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                x, y = x*scale_x, y*scale_y
                if new_game_button.collidepoint((x,y)):
                    return True
                elif load_game_button.collidepoint((x,y)):
                    return False
                
            
def is_correct_game_file():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                x, y = x*scale_x, y*scale_y
                if save_button.collidepoint((x,y)):
                    return False
                elif undo_button.collidepoint((x,y)):
                    return True
                
                
def review_command():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                x, y = x*scale_x, y*scale_y
                if save_button.collidepoint((x,y)):
                    return "progress"
                elif undo_button.collidepoint((x,y)):
                    return "undo"
                elif hint_button.collidepoint((x,y)):
                    return "quit"
                elif move_button.collidepoint((x,y)):
                    return "move"
                
            
    
               