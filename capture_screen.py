# capture_screen.py

from selenium import webdriver
from PIL import Image
import time
import config
import os
import cv2
import numpy as np


def capture_screen(driver, save_path='full_screen.png'):
    """Capture une capture d'écran complète et détecte automatiquement la grille."""
    print("Ajustement de la taille de la fenêtre pour capturer toute la page...")

    # Utiliser JavaScript pour obtenir la hauteur totale de la page
    total_width = driver.execute_script("return document.body.scrollWidth")
    total_height = driver.execute_script("return document.body.scrollHeight")

    # Ajuster la taille de la fenêtre
    driver.set_window_size(total_width, total_height)
    time.sleep(2)  # Attendre que la fenêtre se redimensionne

    print(f"Taille de la fenêtre ajustée à {total_width}x{total_height} pixels.")

    # Scroll to center (optional, for better capture)
    driver.execute_script("window.scrollTo(arguments[0], arguments[1]);", total_width // 2, total_height // 2)
    time.sleep(1)

    print("Capture de l'écran en cours...")
    # Prendre une capture d'écran complète
    driver.save_screenshot(save_path)

    print(f"Capture d'écran complète sauvegardée à : {save_path}")
    return save_path


def detect_grid(image_path):
    """Détecte la grille 2048 dans l'image en se basant sur la couleur du bord."""
    print("Détection de la grille dans l'image...")

    # Lire l'image avec OpenCV
    image = cv2.imread(image_path)
    if image is None:
        print(f"Erreur : Impossible de lire l'image {image_path}")
        return None

    # Convertir la couleur de l'image de BGR à RGB
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Définir la couleur du bord en BGR
    border_color = config.GRID_BORDER_COLOR  # (B, G, R)

    # Définir la plage de tolérance
    lower = np.array([c - config.COLOR_TOLERANCE for c in border_color])
    upper = np.array([c + config.COLOR_TOLERANCE for c in border_color])

    # Créer un masque pour les pixels de la couleur du bord
    mask = cv2.inRange(image, lower, upper)

    # Trouver les contours dans le masque
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if not contours:
        print("Erreur : Aucune grille détectée.")
        return None

    # Supposer que le plus grand contour est la grille
    largest_contour = max(contours, key=cv2.contourArea)

    # Obtenir le rectangle englobant
    x, y, w, h = cv2.boundingRect(largest_contour)

    print(f"Grille détectée à la position x:{x}, y:{y}, largeur:{w}, hauteur:{h}")

    # Ajouter un padding si nécessaire
    padding = 10  # pixels
    x = max(x - padding, 0)
    y = max(y - padding, 0)
    w = min(w + 2 * padding, image.shape[1] - x)
    h = min(h + 2 * padding, image.shape[0] - y)

    # Découper la grille de l'image
    grid_image = image[y:y + h, x:x + w]
    grid_image_pil = Image.fromarray(cv2.cvtColor(grid_image, cv2.COLOR_BGR2RGB))

    grid_image_path = os.path.join(config.CACHE_FOLDER, 'grid.png')
    grid_image_pil.save(grid_image_path)

    print(f"Capture de la grille sauvegardée à : {grid_image_path}")
    return grid_image_path
