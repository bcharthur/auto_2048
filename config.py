# config.py
import os

CHROME_DRIVER_PATH = 'C:/chromedriver-win64/chromedriver.exe'
CACHE_FOLDER = 'cache'
LOG_FOLDER = 'log'
LOGGER_FILE = os.path.join(LOG_FOLDER, 'logger.txt')
MOVEMENTS_FILE = os.path.join(LOG_FOLDER, '2048.txt')
GAME_URL = 'https://play2048.co/'
GRID_BORDER_COLOR = (123, 138, 155)

TILE_COLORS = {
    '2': '#eee4da',
    '4': '#ebd8b6',
    '8': '#f2b076',
    '16': '#f6905c',
    '32': '#f77f63',
    '64': '#f76442',
    '128': '#f1d26b',
    '256': '#f1d26b',
    '512': '#f1d26b',
    '1024': '#f1d26b',
    '2048': '#f1d26b',
}

def hex_to_bgr(hex_color):
    hex_color = hex_color.lstrip('#')
    rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    return (rgb[2], rgb[1], rgb[0])

TILE_COLORS_BGR = {value: hex_to_bgr(color) for value, color in TILE_COLORS.items()}

for folder in [CACHE_FOLDER, LOG_FOLDER]:
    if not os.path.exists(folder):
        os.makedirs(folder)
