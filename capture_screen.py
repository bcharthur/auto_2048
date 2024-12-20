# capture_screen.py
from selenium import webdriver
import time
import config
import os
import cv2
import numpy as np
from logger_setup import logger


def capture_screen(driver, save_path='cache/full_screen.png'):
    logger.info("Capture de l'écran en cours...")
    driver.save_screenshot(save_path)
    logger.info(f"Capture d'écran complète sauvegardée à : {save_path}")
    return save_path


def detect_grid(image_path):
    logger.info("Détection de la grille dans l'image...")
    image = cv2.imread(image_path)
    if image is None:
        logger.error(f"Impossible de lire l'image {image_path}")
        return None

    # Détection simplifiée
    # On suppose que la grille est détectée par couleur du bord
    # Ajuster selon le site
    # Ici, on fait comme avant, code simplifié
    # ...
    # Retour du path grid si trouvé

    # Pour simplifier, on prend le rectangle déjà connu (par exemple positions fixes)
    # Ou réimplémenter la détection comme dans votre code précédent.
    # Pour ce code, on suppose qu'on a déjà les routines :

    # Code d'exemple, à adapter selon vos besoins.
    # On suppose qu'on a récupéré x,y,w,h pour la grille
    # (exemple repris du code fourni, ajuster si besoin)
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    # Recherche du contour le plus grand comme avant
    # Pour rester cohérent, je reprends le code de détection initial si vous l'aviez :

    border_color_bgr = config.GRID_BORDER_COLOR
    border_color_hsv = cv2.cvtColor(np.uint8([[border_color_bgr]]), cv2.COLOR_BGR2HSV)[0][0]
    lower = np.array([border_color_hsv[0] - 10, max(border_color_hsv[1] - 50, 50), max(border_color_hsv[2] - 50, 50)])
    upper = np.array([border_color_hsv[0] + 10, 255, 255])
    mask = cv2.inRange(hsv, lower, upper)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        logger.error("Aucune grille détectée.")
        return None
    largest_contour = max(contours, key=cv2.contourArea)
    x, y, w, h = cv2.boundingRect(largest_contour)
    logger.info(f"Grille détectée à la position x:{x}, y:{y}, largeur:{w}, hauteur:{h}")
    padding = 10
    x = max(x - padding, 0)
    y = max(y - padding, 0)
    w = min(w + 2 * padding, image.shape[1] - x)
    h = min(h + 2 * padding, image.shape[0] - y)

    grid_image = image[y:y + h, x:x + w]
    grid_image_pil_path = os.path.join(config.CACHE_FOLDER, 'grid.png')
    cv2.imwrite(grid_image_pil_path, grid_image)
    logger.info(f"Capture de la grille sauvegardée à : {grid_image_pil_path}")
    return grid_image_pil_path
