# analyze_screen.py

import easyocr
from PIL import Image, ImageDraw, ImageFont
import config
import os

# Initialiser EasyOCR avec le français
reader = easyocr.Reader(['fr'], gpu=False)

def detect_grid_cells(image_path: str):
    """
    Détecte les chiffres dans la grille 2048 et retourne une matrice 4x4 représentant l'état du jeu.

    :param image_path: Chemin de l'image de la grille.
    :return: Grille 4x4 avec les valeurs des tuiles.
    """
    print("Analyse de l'image pour détecter la grille...")

    # Lire le texte dans l'image
    result = reader.readtext(image_path)
    print("Résultats OCR :", result)

    # Ouvrir l'image avec PIL
    image_pil = Image.open(image_path)
    draw = ImageDraw.Draw(image_pil)

    # Charger une police de caractères
    try:
        font = ImageFont.truetype("arial.ttf", 20)
    except IOError:
        font = ImageFont.load_default()

    # Initialiser la grille
    grid = [[0 for _ in range(4)] for _ in range(4)]

    # Dimensions de la grille
    grid_image = image_pil.convert('RGB')
    grid_width, grid_height = grid_image.size
    cell_size_x = grid_width / 4
    cell_size_y = grid_height / 4

    # Parcourir les résultats et dessiner les annotations
    for detection in result:
        bbox, text, confidence = detection
        # bbox est une liste de 4 points [haut-gauche, haut-droit, bas-droit, bas-gauche]
        haut_gauche, haut_droit, bas_droit, bas_gauche = bbox
        mot_clean = ''.join(filter(str.isdigit, text))
        if not mot_clean:
            continue
        digit = int(mot_clean)

        # Calculer le centre de la tuile
        x_center = sum([point[0] for point in bbox]) / 4
        y_center = sum([point[1] for point in bbox]) / 4

        # Déterminer la position dans la grille
        col = int(x_center / cell_size_x)
        row = int(y_center / cell_size_y)

        if 0 <= row < 4 and 0 <= col < 4:
            grid[row][col] = digit
            print(f"Tuile détectée : {digit} à la position ({row}, {col})")

            # Dessiner un rectangle vert autour du chiffre
            draw.rectangle([haut_gauche[0], haut_gauche[1], bas_droit[0], bas_droit[1]], outline=(0, 255, 0), width=2)
            draw.text((haut_gauche[0] + 5, bas_droit[1] - 25), mot_clean, fill=(255, 255, 255), font=font)

    # Sauvegarder l'image annotée
    detection_image_path = os.path.join(config.CACHE_FOLDER, "screen_detection.png")
    image_pil.save(detection_image_path)
    print(f"Image de détection sauvegardée à : {detection_image_path}")

    # Afficher la grille détectée
    print("Grille détectée :")
    for row in grid:
        print(row)

    return grid
