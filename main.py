# main.py

import connect_accept_cookies
import capture_screen
import analyze_screen
import config
from selenium import webdriver
import time

def main():
    print("Démarrage du script principal...")

    # Initialiser le driver Selenium
    driver = connect_accept_cookies.initialize_driver()

    try:
        # Se connecter au site et accepter les cookies
        connect_accept_cookies.connect_and_accept_cookies(driver)
        print("Étape 1 : Connexion et acceptation des cookies terminée.")

        # Attendre un peu pour s'assurer que la page est complètement chargée
        time.sleep(2)

        # Capturer la capture d'écran complète
        full_screen_path = capture_screen.capture_screen(driver)
        print("Étape 2 : Capture d'écran complète terminée.")

        # Détecter et capturer la grille
        grid_image_path = capture_screen.detect_grid(full_screen_path)
        if not grid_image_path:
            print("Étape 3 : Détection de la grille échouée.")
            return
        print("Étape 3 : Détection de la grille terminée.")

        # Analyser la capture d'écran de la grille
        grid = analyze_screen.detect_grid_cells(grid_image_path)
        print("Étape 4 : Analyse de l'écran terminée.")

        # Afficher la grille finale
        print("Grille finale détectée :")
        for row in grid:
            print(row)

    except Exception as e:
        print("Une erreur est survenue :", e)
    finally:
        # Fermer le driver Selenium
        driver.quit()
        print("Driver Selenium fermé.")

if __name__ == "__main__":
        main()
