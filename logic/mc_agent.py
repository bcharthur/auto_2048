import random
import copy
from logic.game import is_move_possible, move_grid
from logic.move_simulation import simulate_move, get_empty_cells, add_tile
from logic.evaluation import evaluate_grid

def get_best_move(grid, runs=50):
    """
    Détermine le meilleur coup en testant chaque direction.
    Pour chaque coup possible, lance 'runs' simulations aléatoires (randomRun).
    Retourne le mouvement (string) : 'up', 'right', 'down', 'left'.
    """
    directions = ['up', 'right', 'down', 'left']
    best_move = None
    best_score = -float('inf')

    for i, move in enumerate(directions):
        if is_move_possible(grid, move):
            score = multi_random_run(grid, move, runs)
            if score > best_score:
                best_score = score
                best_move = move

    return best_move

def multi_random_run(grid, direction, runs):
    """
    Lance 'runs' randomRun pour un coup initial donné et calcule le score moyen.
    """
    total_score = 0
    success_runs = 0
    for _ in range(runs):
        res = random_run(grid, direction)
        if res != -1:
            total_score += res
            success_runs += 1

    if success_runs == 0:
        return -1
    return total_score / success_runs

def random_run(grid, direction):
    """
    Simule une partie depuis le coup initial 'direction'.

    Étapes :
    1. Cloner la grille.
    2. Appliquer le coup initial. Si pas possible, retourner -1.
    3. Ajouter une tuile au hasard (comme dans le jeu).
    4. Tant que des coups sont possibles, choisir un coup aléatoire, l'appliquer,
       ajouter une tuile si le coup a changé la grille, accumuler le score.
    5. Quand plus aucun mouvement n'est possible, retourner le score final de la grille.

    Ici, le "score" peut être la valeur retournée par evaluate_grid, ou la somme des merges.
    On peut cumuler un score plus "classique" en additionnant simplement
    les merges effectuées. On peut aussi évaluer l'état final avec evaluate_grid
    pour refléter la qualité finale du plateau.
    """
    g = copy.deepcopy(grid)

    # Coup initial
    move_result = simulate_move(g, direction)
    if move_result == g:
        # mouvement pas possible
        return -1
    g = move_result
    # Ajouter une tuile
    g = add_random_tile_if_possible(g)

    # Ici, on peut soit accumuler un score à chaque merge,
    # soit juste évaluer la grille finale. Pour simplifier, on cumulera
    # le score via evaluate_grid à la fin. Le code JS cumule le score des merges.
    # On va approximativement simuler un score en stockant les merges.
    # Cependant, le JS code ajoute un score à chaque fusion. Nous n'avons pas
    # l'information facilement. On va donc évaluer la grille finale après plus
    # de coups pour refléter la qualité globale.
    # On peut faire un loop jusqu'à la fin et, au final, retourner evaluate_grid.

    # Continuer jusqu'à plus de moves
    # On joue au hasard : 4 directions possibles.
    moves = ['up', 'right', 'down', 'left']

    # On arrête quand plus aucun mouvement n'est possible
    while any(is_move_possible(g, m) for m in moves):
        # Choisir un move aléatoire
        random_move = random.choice(moves)
        if is_move_possible(g, random_move):
            new_g = simulate_move(g, random_move)
            if new_g != g:
                g = new_g
                # Ajouter une tuile
                g = add_random_tile_if_possible(g)
        # Si le move est pas possible, on refait un choix au prochain tour
        # ou on finit par un no move possible

    # A la fin, on retourne evaluate_grid comme proxy de score
    final_score = evaluate_grid(g)
    return final_score

def add_random_tile_if_possible(grid):
    empty = get_empty_cells(grid)
    if not empty:
        return grid
    # 90% 2, 10% 4
    position = random.choice(empty)
    value = 2 if random.random() < 0.9 else 4
    return add_tile(grid, position, value)
