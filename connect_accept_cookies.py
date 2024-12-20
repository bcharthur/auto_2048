# connect_accept_cookies.py
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import config
import time
from logger_setup import logger

def initialize_driver():
    service = Service(config.CHROME_DRIVER_PATH)
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(service=service, options=options)
    logger.info("Driver Selenium initialisé.")
    return driver

def connect_and_accept_cookies(driver):
    logger.info("Connexion au site...")
    driver.get(config.GAME_URL)

    try:
        wait = WebDriverWait(driver, 10)
        cookie_dialog = wait.until(EC.presence_of_element_located((By.ID, "ez-cookie-dialog")))
        logger.info("Dialog des cookies trouvé.")
        accept_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Utilisez les cookies nécessaires uniquement et continuez')]")
        accept_button.click()
        logger.info("Cookies acceptés.")
    except Exception as e:
        logger.warning(f"Aucun bouton d'acceptation des cookies trouvé ou une erreur est survenue : {e}")
    time.sleep(2)
