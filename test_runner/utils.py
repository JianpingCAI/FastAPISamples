# utils.py
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def log_debug(message):
    logging.debug(message)


def log_info(message):
    logging.info(message)


def log_error(message):
    logging.error(message, exc_info=True)  # Include traceback information


import psutil


def get_system_metrics():
    cpu_usage = psutil.cpu_percent(interval=1)
    memory_usage = psutil.virtual_memory().percent
    return {"cpu_usage": cpu_usage, "memory_usage": memory_usage}
