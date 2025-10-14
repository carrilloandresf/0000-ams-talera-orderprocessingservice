import logging
from pythonjsonlogger import jsonlogger
from .config import settings

def configure_logging() -> None:
    logger = logging.getLogger()
    logger.setLevel(settings.log_level)

    handler = logging.StreamHandler()
    formatter = jsonlogger.JsonFormatter('%(asctime)s %(levelname)s %(name)s %(message)s')
    handler.setFormatter(formatter)

    # limpia handlers duplicados
    logger.handlers = []
    logger.addHandler(handler)
