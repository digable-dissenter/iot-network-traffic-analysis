import datetime
import logging
from logging.handlers import RotatingFileHandler
import os

def setup_logger():
    logger = logging.getLogger('etl_logger')
    
    if not logger.hasHandlers():
        logger.setLevel(logging.DEBUG)

        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        log_dir = 'logs'
        os.makedirs(log_dir, exist_ok=True) # Create the directory if it doesn't exist
        log_file = os.path.join(log_dir, f'etl_process_{timestamp}.log') # Construct the full log file path

        # Create rotating file handler
        fh = RotatingFileHandler(log_file, maxBytes=5*1024*1024, backupCount=3)
        fh.setLevel(logging.DEBUG)

        # Create console handler
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)

        # Create formatter and add it to the handlers
        formatter = logging.Formatter(fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                                      datefmt='%m-%d-%y %H:%M:%S')
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)

        # Add the handlers to the logger
        logger.addHandler(fh)
        logger.addHandler(ch)

    return logger