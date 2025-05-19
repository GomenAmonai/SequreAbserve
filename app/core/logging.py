import sys, logging
from loguru import logger
from pythonjsonlogger import jsonlogger

def setup_logging():
    # логuru → stdout
    logger.remove()
    logger.add(sys.stdout, level="INFO", backtrace=False, diagnose=False,
               format="{time} | {level} | {message}")

    # стандартный logging → JSON (подхватится systemd / Docker-driver)
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(jsonlogger.JsonFormatter())
    root = logging.getLogger()
    root.setLevel(logging.INFO)
    root.handlers = [handler]