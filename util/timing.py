import time
from functools import wraps
from logging_config.logging_config import setup_logger

logger = setup_logger()

def log_execution_time(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        duration = end_time - start_time
        logger.info(f"Executed {func.__name__} in {duration:.4f} seconds.")
        return result
    return wrapper