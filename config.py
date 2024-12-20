# config.py

import os

# Chemins
CHROME_DRIVER_PATH = 'C:/chromedriver-win64/chromedriver.exe'  # Remplacez par le chemin réel
CACHE_FOLDER = 'cache'

# URL du jeu
GAME_URL = 'https://play2048.co/'

# Couleur du bord de la grille (BGR pour OpenCV)
GRID_BORDER_COLOR = (123, 138, 155)  # Converti de #9b8a7b à (123, 138, 155) en BGR

# Tolerance de couleur pour la détection du bord de la grille
COLOR_TOLERANCE = 30  # Ajustez cette valeur si nécessaire

# Créer le dossier 'cache' s'il n'existe pas
if not os.path.exists(CACHE_FOLDER):
    os.makedirs(CACHE_FOLDER)
