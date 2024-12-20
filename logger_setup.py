# logger_setup.py
import logging
import config

logger = logging.getLogger('2048_logger')
logger.setLevel(logging.DEBUG)

fh = logging.FileHandler(config.LOGGER_FILE)
fh.setLevel(logging.DEBUG)

mh = logging.FileHandler(config.MOVEMENTS_FILE)
mh.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
mh.setFormatter(formatter)

logger.addHandler(fh)
logger.addHandler(mh)

logging.getLogger().handlers = []
