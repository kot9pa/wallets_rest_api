import logging

from src.config import settings


def get_logger(level=None):
    logger = logging.getLogger('uvicorn.error')
    logger.setLevel(level or logging.DEBUG)
    return logger


logger = get_logger(settings.LOG_LEVEL.upper())
