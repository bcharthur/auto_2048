# send_move.py
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
from logger_setup import logger

def send_move(driver, move):
    move_key = {
        'up': Keys.ARROW_UP,
        'down': Keys.ARROW_DOWN,
        'left': Keys.ARROW_LEFT,
        'right': Keys.ARROW_RIGHT
    }
    if move not in move_key:
        logger.error(f"Mouvement invalide: {move}")
        return False
    try:
        body = driver.find_element(By.TAG_NAME, 'body')
        body.send_keys(move_key[move])
        logger.info(f"Mouvement envoyé: {move}")
        time.sleep(0.1)
        return True
    except Exception as e:
        logger.error(f"Erreur lors de l'envoi du mouvement {move}: {e}")
        return False
