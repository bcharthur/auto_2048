# logic/game.py
import copy

def transpose(grid):
    return [list(row) for row in zip(*grid)]

def reverse_rows(grid):
    return [row[::-1] for row in grid]

def compress_left(grid):
    new_grid = []
    for row in grid:
        filtered = [x for x in row if x != 0]
        merged = []
        skip = False
        for i in range(len(filtered)):
            if skip:
                skip = False
                continue
            if i+1 < len(filtered) and filtered[i] == filtered[i+1]:
                merged.append(filtered[i]*2)
                skip = True
            else:
                merged.append(filtered[i])
        merged += [0]*(4-len(merged))
        new_grid.append(merged)
    return new_grid

def move_left(grid):
    return compress_left(grid)

def move_right(grid):
    reversed_grid = reverse_rows(grid)
    new_grid = compress_left(reversed_grid)
    return reverse_rows(new_grid)

def move_up(grid):
    transposed = transpose(grid)
    moved = compress_left(transposed)
    return transpose(moved)

def move_down(grid):
    transposed = transpose(grid)
    reversed_grid = reverse_rows(transposed)
    moved = compress_left(reversed_grid)
    moved = reverse_rows(moved)
    return transpose(moved)

def move_grid(grid, direction):
    if direction == 'up':
        return move_up(grid)
    elif direction == 'down':
        return move_down(grid)
    elif direction == 'left':
        return move_left(grid)
    elif direction == 'right':
        return move_right(grid)
    else:
        return grid

def is_move_possible(grid, direction):
    new_grid = move_grid(copy.deepcopy(grid), direction)
    return new_grid != grid
