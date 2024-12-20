# logic/__init__.py
from .game import move_grid, is_move_possible
from .evaluation import evaluate_grid
from .move_simulation import simulate_move, get_empty_cells, add_tile
# On garde expectimax pour éventuelles comparaisons, même si on utilise Q-learning
from .expectimax import determine_next_move, expectimax
