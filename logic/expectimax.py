# logic/expectimax.py
# Resté inchangé, au besoin. On se concentre sur le mc_agent.

import math
from logic.evaluation import evaluate_grid
from logic.move_simulation import simulate_move, get_empty_cells, add_tile
from logic.game import is_move_possible

PROBABILITIES = {2:0.9,4:0.1}

def determine_next_move(board, depth=4):
    best_move = None
    best_score = -math.inf
    for move in ['up','down','left','right']:
        if is_move_possible(board,move):
            new_board = simulate_move(board,move)
            score = expectimax(new_board, depth-1, False)
            if score > best_score:
                best_score = score
                best_move = move
    return best_move

def expectimax(board, depth, is_max_player):
    if depth == 0:
        return evaluate_grid(board)
    empty = get_empty_cells(board)
    if not empty:
        return evaluate_grid(board)

    if is_max_player:
        max_score = -math.inf
        for move in ['up','down','left','right']:
            if is_move_possible(board,move):
                new_board = simulate_move(board,move)
                score = expectimax(new_board, depth-1, False)
                if score > max_score:
                    max_score = score
        return max_score
    else:
        total_score = 0
        count = len(empty)*len(PROBABILITIES)
        if count == 0:
            return evaluate_grid(board)
        for position in empty:
            for value,prob in PROBABILITIES.items():
                new_board = add_tile(board,position,value)
                score = expectimax(new_board, depth-1, True)
                total_score += prob*score
        return total_score
