# logic/evaluation.py
from logger_setup import logger
import math

def evaluate_grid(grid):
    """
    Évalue la grille selon plusieurs critères pour encourager la réduction du nombre de tuiles,
    le rapprochement de tuiles de même valeur, la monotonie, et la place pour la croissance.

    Critères :
    - Nombre de tuiles vides (incite à garder la grille libre).
    - Monotonie (préférence pour un ordre décroissant).
    - Coalescence (récompense les tuiles adjacentes identiques).
    - Regroupement (tuiles semblables proches).
    - Bonus si la plus grosse tuile est dans un coin.

    Ajustez les pondérations selon les résultats.
    """
    empty_tiles = sum(row.count(0) for row in grid)
    score = empty_tiles * 100

    # Monotonie
    mono_score = 0
    for i in range(4):
        for j in range(3):
            if grid[i][j] >= grid[i][j+1]:
                mono_score += (grid[i][j] - grid[i][j+1])
    for j in range(4):
        for i in range(3):
            if grid[i][j] >= grid[i+1][j]:
                mono_score += (grid[i][j] - grid[i+1][j])

    score += mono_score * 0.1

    # Coalescence
    coalescence = 0
    for i in range(4):
        for j in range(4):
            val = grid[i][j]
            if val == 0:
                continue
            # Droite
            if j < 3 and grid[i][j] == grid[i][j+1]:
                coalescence += val*2
            # Bas
            if i < 3 and grid[i][j] == grid[i+1][j]:
                coalescence += val*2
    score += coalescence

    # Regroupement
    positions_by_value = {}
    for i in range(4):
        for j in range(4):
            val = grid[i][j]
            if val > 0:
                if val not in positions_by_value:
                    positions_by_value[val] = []
                positions_by_value[val].append((i,j))

    grouping_score = 0
    for val, positions in positions_by_value.items():
        if len(positions) > 1:
            dist_sum = 0
            count = 0
            for p in range(len(positions)):
                for q in range(p+1, len(positions)):
                    pi = positions[p]
                    pj = positions[q]
                    dist = abs(pi[0]-pj[0]) + abs(pi[1]-pj[1])
                    dist_sum += dist
                    count += 1
            if count > 0:
                avg_dist = dist_sum / count
                grouping_score += max(0, 10 - avg_dist)*5

    score += grouping_score

    # Bonus max tile in corner
    max_tile = max(max(row) for row in grid)
    corners = [grid[0][0], grid[0][3], grid[3][0], grid[3][3]]
    if max_tile in corners:
        score += 500

    return score
