import card_file
import piece_file
import move_file
import game_state_file
import numpy as np

def test_update_future_possible_moves_1():
    p1 = piece_file.piece((0,0),False,False)
    c1 = (card_file.card.create_card("Tiger"))
    tester = p1.update_future_possible_moves(c1)
    assert tester[0].target == (2,0) and tester[1].target == (-1,0) and len(tester) == 2

def test_update_future_possible_moves_2():
    p1 = piece_file.piece((-1,-2),True,False)
    c1 = (card_file.card.create_card("Elephant"))
    tester = p1.update_future_possible_moves(c1)
    assert tester[0].target == (-2,-1) and tester[1].target == (-1,-1) and len(tester) == 2

def test_update_future_possible_moves_3():
    p1 = piece_file.piece((0,0),True,False)
    c1 = (card_file.card.create_card("Cobra"))
    tester = p1.update_future_possible_moves(c1)
    assert tester[0].target == (-1,1) and tester[1].target == (0,-1) and tester[2].target == (1,1) and len(tester) == 3

def create_pieces(n,coordinates,is_b,is_m):
    lst = []
    for i in range(n):
        piece = piece_file.piece(coordinates[i],is_b[i],is_m[i])
        
        lst.append(piece)

    return lst


def create_game_state(b_pieces,r_pieces,b_cards,r_cards,m_card,is_b):
    return game_state_file.game_state(b_pieces,r_pieces,b_cards,r_cards,m_card,is_b)

def test_generate_possible_moves_1():
    b_pieces = create_pieces(2,[(1,1),(-1,2)],[True,True],[True,False])
    r_pieces = create_pieces(2,[(0,1),(-1,0)],[False,False],[True,False])
    g1 = create_game_state(b_pieces,r_pieces,[card_file.card.create_card("Elephant"),card_file.card.create_card("Crab")],[card_file.card.create_card("Frog"),card_file.card.create_card("Rooster")],card_file.card.create_card("Horse"),False)
    g1.b_pieces = [piece.next_moves(g1.player_b_cards) for piece in g1.player_b_pieces]
    g1.r_pieces = [piece.next_moves(g1.player_r_cards) for piece in g1.player_r_pieces]
    assert len(g1.generate_possible_moves()) == 11 # do some write up stuff