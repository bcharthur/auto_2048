# logic/move_simulation.py
import copy
from logic.game import move_grid

def simulate_move(grid, direction):
    return move_grid(copy.deepcopy(grid), direction)

def get_empty_cells(grid):
    empty = []
    for i in range(4):
        for j in range(4):
            if grid[i][j] == 0:
                empty.append((i, j))
    return empty

def add_tile(grid, position, value):
    new_grid = copy.deepcopy(grid)
    new_grid[position[0]][position[1]] = value
    return new_grid
