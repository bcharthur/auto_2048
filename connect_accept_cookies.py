# connect_accept_cookies.py

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import config
import time

def initialize_driver():
    """Initialise le driver Selenium."""
    service = Service(config.CHROME_DRIVER_PATH)
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")  # Ouvrir le navigateur en mode maximisé
    driver = webdriver.Chrome(service=service, options=options)
    return driver

def connect_and_accept_cookies(driver):
    """Se connecte au site et accepte les cookies."""
    print("Connexion au site...")
    driver.get(config.GAME_URL)

    try:
        # Attendre que le dialog des cookies soit présent
        wait = WebDriverWait(driver, 10)
        cookie_dialog = wait.until(EC.presence_of_element_located((By.ID, "ez-cookie-dialog")))
        print("Dialog des cookies trouvé.")

        # Cliquer sur le bouton "Utilisez les cookies nécessaires uniquement et continuez"
        accept_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Utilisez les cookies nécessaires uniquement et continuez')]")
        accept_button.click()
        print("Cookies acceptés.")
    except Exception as e:
        print("Aucun bouton d'acceptation des cookies trouvé ou une erreur est survenue :", e)

    # Attendre un peu pour s'assurer que l'action est complétée
    time.sleep(2)
