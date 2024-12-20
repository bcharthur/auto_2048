# analyze_screen.py
import easyocr
from PIL import Image, ImageDraw, ImageFont
import config
import os
import cv2
import numpy as np
from logger_setup import logger

reader = easyocr.Reader(['en'], gpu=False)

def detect_grid_cells(image_path: str):
    """
    Détecte les tuiles dans la grille 2048 (4x4) en utilisant OCR.
    Retourne une matrice 4x4 avec les valeurs détectées.
    """
    logger.info("Analyse de l'image pour détecter la grille...")

    image_cv = cv2.imread(image_path)
    if image_cv is None:
        logger.error(f"Impossible de lire l'image {image_path}")
        return [[0]*4 for _ in range(4)]

    result = reader.readtext(image_path, detail=1, paragraph=False)
    logger.debug(f"Résultats OCR : {result}")

    image_pil = Image.open(image_path)
    draw = ImageDraw.Draw(image_pil)
    try:
        font = ImageFont.truetype("arial.ttf", 20)
    except IOError:
        font = ImageFont.load_default()

    grid = [[0 for _ in range(4)] for _ in range(4)]
    grid_width, grid_height = image_pil.size
    cell_size_x = grid_width / 4
    cell_size_y = grid_height / 4

    for detection in result:
        bbox, text, confidence = detection
        mot_clean = ''.join(filter(str.isdigit, text))
        if not mot_clean:
            continue
        try:
            digit = int(mot_clean)
        except ValueError:
            digit = None

        x_center = sum([point[0] for point in bbox]) / 4
        y_center = sum([point[1] for point in bbox]) / 4

        col = int(x_center / cell_size_x)
        row = int(y_center / cell_size_y)

        if 0 <= row < 4 and 0 <= col < 4 and digit is not None:
            grid[row][col] = digit
            draw.rectangle([bbox[0][0], bbox[0][1], bbox[2][0], bbox[2][1]], outline=(0, 255, 0), width=2)
            draw.text((bbox[0][0] + 5, bbox[2][1] - 25), mot_clean, fill=(255, 255, 255), font=font)

    detection_image_path = os.path.join(config.CACHE_FOLDER, "screen_detection.png")
    image_pil.save(detection_image_path)
    logger.info(f"Image de détection sauvegardée à : {detection_image_path}")

    logger.debug("Grille détectée :")
    for row in grid:
        logger.debug(row)

    return grid
