import logging
from typing import Callable

from fastapi import FastAPI
from app.core.config import get_settings

logger = logging.getLogger(__name__)


def _startup_model(app) -> None:
    settings = get_settings()
    logger.info("load model complete")
    logger.info("Boostrap neo4j.")


def start_app_handler(app: FastAPI) -> Callable:
    def startup() -> None:
        logger.info("Running app start handler.")
        _startup_model(app)

    return startup


def stop_app_handler() -> Callable:
    def shutdown() -> None:
        logger.info("Running app shutdown handler.")

    return shutdown
