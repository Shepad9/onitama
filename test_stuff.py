#-----------test_stuff.py-----------

import card_file
import piece_file
import move_file
import game_state_file
import game_file
import player_file
import numpy as np

def test_update_future_possible_moves_1():
    p1 = piece_file.piece((0,0),False,False)
    c1 = (card_file.card.create_card("Tiger"))
    tester = p1.update_future_possible_moves(c1)
    assert tester[0].target == (1,0) and tester[1].target == (-2,0) and len(tester) == 2

def test_update_future_possible_moves_2():
    p1 = piece_file.piece((-1,-2),True,False)
    c1 = (card_file.card.create_card("Elephant"))
    tester = p1.update_future_possible_moves(c1)
    assert tester[1].target == (0,-1) and tester[0].target == (-1,-1) and len(tester) == 2

def test_update_future_possible_moves_3():
    p1 = piece_file.piece((0,0),True,False)
    c1 = (card_file.card.create_card("Cobra"))
    tester = p1.update_future_possible_moves(c1)
    assert tester[0].target == (-1,-1) and tester[1].target == (0,1) and tester[2].target == (1,-1) and len(tester) == 3

def create_pieces(n,coordinates,is_b,is_m):
    lst = []
    for i in range(n):
        piece = piece_file.piece(coordinates[i],is_b[i],is_m[i])
        
        lst.append(piece)

    return lst


def create_game_state(b_pieces,r_pieces,b_cards,r_cards,m_card,is_b):
    return game_state_file.game_state(b_pieces,r_pieces,b_cards,r_cards,m_card,is_b)

def create_g1() -> game_state_file.game_state: # standard 2 pieces per colour
    b_pieces = create_pieces(2,[(1,1),(-1,2)],[True,True],[True,False])
    r_pieces = create_pieces(2,[(0,1),(-1,0)],[False,False],[True,False])
    g1 = create_game_state(b_pieces,r_pieces,[card_file.card.create_card("Elephant"),card_file.card.create_card("Crab")],[card_file.card.create_card("Frog"),card_file.card.create_card("Rooster")],card_file.card.create_card("Horse"),False)
    for piece in r_pieces:
        piece.future_possible_moves = piece.next_moves(g1.player_r_cards)
    for piece in b_pieces:
        piece.future_possible_moves = piece.next_moves(g1.player_b_cards)
    return g1

def create_g2() -> game_state_file.game_state: # 2 pieces blue, no pieces red
    b_pieces = create_pieces(2,[(1,1),(-1,2)],[True,True],[True,False])
    r_pieces = create_pieces(0,[],[],[])
    g1 = create_game_state(b_pieces,r_pieces,[card_file.card.create_card("Elephant"),card_file.card.create_card("Crab")],[card_file.card.create_card("Frog"),card_file.card.create_card("Rooster")],card_file.card.create_card("Horse"),False)
    for piece in r_pieces:
        piece.future_possible_moves = piece.next_moves(g1.player_r_cards)
    for piece in b_pieces:
        piece.future_possible_moves = piece.next_moves(g1.player_b_cards)
    return g1

def create_g3() -> game_state_file.game_state: #blue win no red master
    b_pieces = create_pieces(2,[(1,1),(-1,2)],[True,True],[True,False])
    r_pieces = create_pieces(1,[(2,2)],[False],[False])
    g1 = create_game_state(b_pieces,r_pieces,[card_file.card.create_card("Elephant"),card_file.card.create_card("Crab")],[card_file.card.create_card("Frog"),card_file.card.create_card("Rooster")],card_file.card.create_card("Horse"),True)
    for piece in r_pieces:
        piece.future_possible_moves = piece.next_moves(g1.player_r_cards)
    for piece in b_pieces:
        piece.future_possible_moves = piece.next_moves(g1.player_b_cards)
    return g1

def create_g4() -> game_state_file.game_state: # red win, master in temple
    b_pieces = create_pieces(2,[(1,1),(-1,2)],[True,True],[True,False])
    r_pieces = create_pieces(2,[(-2,0),(1,-2)],[False,False],[True,False])
    g1 = create_game_state(b_pieces,r_pieces,[card_file.card.create_card("Elephant"),card_file.card.create_card("Crab")],[card_file.card.create_card("Frog"),card_file.card.create_card("Rooster")],card_file.card.create_card("Horse"),False)
    for piece in r_pieces:
        piece.future_possible_moves = piece.next_moves(g1.player_r_cards)
    for piece in b_pieces:
        piece.future_possible_moves = piece.next_moves(g1.player_b_cards)
    return g1

def test_generate_possible_moves_1():
    g1 = create_g1()
    print(len(g1.generate_possible_moves()))
    assert len(g1.generate_possible_moves()) == 12

def test_find_master_1():
    g1 = create_g1()
    assert g1.get_master_coordinates() == (0,1)

def test_find_master_2():
    g1 = create_g1()
    assert g1.get_master_coordinates(True) == (1,1)

def test_find_master_3():
    g2 = create_g2()
    assert g2.get_master_coordinates(False) == None

def test_find_master_4():
    g3 = create_g3()
    assert g3.get_master_coordinates(False) == None

def test_is_win_1():
    g1 = create_g1()
    assert g1.is_win() == False

def test_is_win_2():
    g1 = create_g3()
    assert g1.is_win() == True
    
def test_is_win_3():
    g1 = create_g4()
    assert g1.is_win() == True
    
def test_static_eval_1():
    g1 = create_g1()
    g1.update_is_game_live()
    p1 = player_file.computer(True)

    assert p1.static_evaluation(g1) < 128
def test_static_eval_2():
    g1 = create_g3()
    g1.update_is_game_live()
    p1 = player_file.computer(True)

    assert p1.static_evaluation(g1) == 1023
def test_static_eval_3():
    g1 = create_g4()
    g1.update_is_game_live()
    p1 = player_file.computer(True)

    assert p1.static_evaluation(g1) == -1023

def test_is_quiet_1():
    g1 = game_file.load_game("noisy_pos.txt", folder = "test_games").current_game_state
    p1 = player_file.computer(g1.is_b_turn)
    assert p1.is_quiet(g1) == False

def test_is_quiet_2():
    g1 = game_file.load_game("quiet_pos.txt", folder = "test_games").current_game_state
    p1 = player_file.computer(g1.is_b_turn)
    assert p1.is_quiet(g1) == True

def test_move_ordering_heuritic_1():
    p1 = player_file.computer(True)
    assert  p1.move_ordering_heuristic(move_file.move(card_file.card.create_card("Elephant"),(0,0),(-2,0)), True) == -2

def test_move_ordering_heuritic_2():
    p1 = player_file.computer(False)
    assert  p1.move_ordering_heuristic(move_file.move(card_file.card.create_card("Elephant"),(0,0),(-2,0)), False) == 2

def test_heuristic_move_sorter():
    p1 = player_file.computer(False)
    m1 = move_file.move(card_file.card.create_card("Elephant"),(0,0),(-2,0))
    m2 = move_file.move(card_file.card.create_card("Crane"),(2,0),(1,1))
    assert np.all(p1.heuristic_move_sorter(np.array([m1,m2]),False) == np.array([m2,m1]))

