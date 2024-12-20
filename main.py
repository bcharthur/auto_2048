# main.py

import os
import shutil
import config

# Nettoyer les dossiers avant d'importer le logger
for folder in [config.LOG_FOLDER, config.CACHE_FOLDER]:
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        if os.path.isfile(file_path) or os.path.islink(file_path):
            os.remove(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)

from logger_setup import logger

import connect_accept_cookies
import capture_screen
import analyze_screen
from logic.game import is_move_possible
from logic.evaluation import evaluate_grid
from logic.move_simulation import simulate_move, get_empty_cells, add_tile
import send_move
from selenium.common.exceptions import WebDriverException, NoSuchWindowException
import time
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import random
import copy


def detect_game_over(driver):
    try:
        driver.find_element(By.XPATH, "//div[contains(text(), 'Game Over')]")
        return True
    except NoSuchElementException:
        return False

def add_random_tile_if_possible(grid):
    empty = get_empty_cells(grid)
    if not empty:
        return grid
    position = random.choice(empty)
    value = 2 if random.random()<0.9 else 4
    return add_tile(grid, position, value)

def simulate_random_playout(grid):
    # Simulation jusqu'à la fin en jouant des moves aléatoires
    moves = ['up','right','down','left']
    g = copy.deepcopy(grid)
    while any(is_move_possible(g,m) for m in moves):
        mv = random.choice(moves)
        if is_move_possible(g,mv):
            new_g = simulate_move(g,mv)
            if new_g != g:
                g = new_g
                g = add_random_tile_if_possible(g)
    return evaluate_grid(g)

def random_run(grid, direction):
    # Coup initial
    g = copy.deepcopy(grid)
    new_g = simulate_move(g,direction)
    if new_g == g:
        return -1
    g = new_g
    g = add_random_tile_if_possible(g)
    # puis suite aléatoire
    return simulate_random_playout(g)

def multi_random_run(grid,direction,runs):
    total = 0
    count = 0
    for _ in range(runs):
        s = random_run(grid,direction)
        if s != -1:
            total += s
            count += 1
    if count==0:
        return -1
    return total/count

def get_best_move_mc(grid, runs=50):
    directions = ['up','right','down','left']
    best_move = None
    best_score = -float('inf')
    for move in directions:
        if is_move_possible(grid,move):
            score = multi_random_run(grid,move,runs)
            if score > best_score:
                best_score = score
                best_move = move
    return best_move


def click_play_again(driver):
    # Tente de cliquer sur "Play Again" directement dans le DOM
    # Ajustez XPATH/CSS si nécessaire
    try:
        play_again_button = driver.find_element(By.XPATH, "//a[contains(text(), 'Try again') or contains(text(), 'Play Again')]")
        play_again_button.click()
        time.sleep(2)
        return True
    except NoSuchElementException:
        logger.error("Bouton 'Play Again' introuvable.")
        return False


def main():
    logger.info("Démarrage du script principal...")

    driver = connect_accept_cookies.initialize_driver()
    connect_accept_cookies.connect_and_accept_cookies(driver)
    logger.info("Connexion et cookies ok.")
    time.sleep(2)

    num_episodes = 2
    for episode in range(num_episodes):
        logger.info(f"Début de l'épisode {episode+1}")

        if detect_game_over(driver):
            with open(config.MOVEMENTS_FILE,'a') as f:
                f.write(f"Partie terminée avant le début de l'épisode {episode+1}. Game Over détecté.\n")
            if not click_play_again(driver):
                logger.error("Impossible de relancer la partie.")
                break
            time.sleep(2)

        full_screen_path = capture_screen.capture_screen(driver)
        grid_image_path = capture_screen.detect_grid(full_screen_path)
        if not grid_image_path:
            logger.error("Détection de la grille échouée. Arrêt.")
            break
        state = analyze_screen.detect_grid_cells(grid_image_path)

        done = False
        total_reward = 0
        old_score = evaluate_grid(state)
        step_count = 0
        episode_moves = []

        while not done:
            # Ici on utilise l'agent Monte Carlo
            move = get_best_move_mc(state, runs=50)
            if move is None:
                # Aucun coup possible
                logger.warning("Aucun mouvement disponible, fin du jeu.")
                done = True
                break

            episode_moves.append(move)
            move_success = send_move.send_move(driver, move)
            time.sleep(0.5)

            full_screen_path_after = capture_screen.capture_screen(driver)
            grid_image_path_after = capture_screen.detect_grid(full_screen_path_after)
            if grid_image_path_after:
                new_state = analyze_screen.detect_grid_cells(grid_image_path_after)
            else:
                new_state = state

            new_score = evaluate_grid(new_state)

            if detect_game_over(driver):
                with open(config.MOVEMENTS_FILE,'a') as f:
                    f.write(f"Game Over détecté. Épisode {episode+1}, Mouvement {step_count+1}, Score final : {new_score}\n")
                reward = -1000
                done = True
            else:
                reward = new_score - old_score
                if new_state == state and move_success:
                    reward -= 10
                if not any(is_move_possible(new_state, m) for m in ['up','down','left','right']):
                    reward -= 500
                    done = True

            # Pas de véritable apprentissage ici, mais on pourrait l'intégrer
            # agent.update(state, action, ... ) si nécessaire

            state = new_state
            old_score = new_score
            total_reward += reward
            step_count += 1

            if done:
                logger.info(f"Fin de l'épisode {episode+1}, total reward: {total_reward}, steps: {step_count}")
                # Logique supplémentaire (logic.txt, score.txt) si nécessaire
                logic_file_path = os.path.join(config.LOG_FOLDER,"logic.txt")
                score_file_path = os.path.join(config.LOG_FOLDER,"score.txt")
                with open(logic_file_path,'a') as lf:
                    lf.write(f"Episode {episode+1}: {episode_moves}\n")
                with open(score_file_path,'a') as sf:
                    sf.write(f"Episode {episode+1}, Score final: {new_score}\n")

                if detect_game_over(driver):
                    if not click_play_again(driver):
                        logger.error("Impossible de relancer après Game Over.")
                break

    driver.quit()
    logger.info("Fin de tous les épisodes, driver fermé.")

if __name__ == "__main__":
    main()
