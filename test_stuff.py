import card
import piece
import move
import numpy as np

def test_update_future_possible_moves_1():
    p1 = piece.piece_obj((0,0),False,False)
    c1 = (card.card_obj.create_card("Tiger"))
    p1.update_future_possible_moves(c1)
    assert p1.future_possible_moves[0].target == (2,0) and p1.future_possible_moves[1].target == (-1,0) and len(p1.future_possible_moves) == 2

def test_update_future_possible_moves_2():
    p1 = piece.piece_obj((-1,-2),True,False)
    c1 = (card.card_obj.create_card("Elephant"))
    p1.update_future_possible_moves(c1)
    assert p1.future_possible_moves[0].target == (-2,-1) and p1.future_possible_moves[1].target == (-1,-1) and len(p1.future_possible_moves) == 2

def test_update_future_possible_moves_3():
    p1 = piece.piece_obj((0,0),True,False)
    c1 = (card.card_obj.create_card("Cobra"))
    p1.update_future_possible_moves(c1)
    assert p1.future_possible_moves[0].target == (-1,1) and p1.future_possible_moves[1].target == (0,-1) and p1.future_possible_moves[2].target == (1,1) and len(p1.future_possible_moves) == 3
