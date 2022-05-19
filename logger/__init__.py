import os
import sys
from logging.handlers import RotatingFileHandler

from loguru import logger


fmt = "<yellow>{time:YYYY-MM-DD at HH:mm:ss}</> | <level>{level:<8}</level> | " \
      "<cyan>{function:<30}:{line:<4}</>: <level>{message}</>"

path_log = os.path.join("logs", 'snake_snake.log')

if not os.path.exists("logs"):
    os.mkdir("logs")

config = {
    "handlers": [
        {
            "sink": sys.stdout,
            "colorize": True,
            "format": fmt,
        },
        {
            "sink": RotatingFileHandler(path_log, maxBytes=10 * 1024 * 1024, backupCount=1, delay=0),
            "backtrace": True,
            "format": fmt
        }
    ],
}

logger.configure(**config)
logging = logger.opt(colors=True)
