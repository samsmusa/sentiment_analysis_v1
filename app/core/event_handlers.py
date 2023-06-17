import logging
from typing import Callable

from fastapi import FastAPI
from app.core.config import settings

logger = logging.getLogger(__name__)


def _startup_model(app) -> None:
    knn_path = settings.KNN_PATH
    tfidf_path = settings.TFIDF_PATH
    model_path = settings.MODEL_PATH
    JobRecommendationModelV1().load_local_model(knn_path, tfidf_path)
    JobRecommendationModelV2().load_local_model(model_path)
    logger.info("load model complete")
    GraphDB.set_connection(database_settings=app.state.config)
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
