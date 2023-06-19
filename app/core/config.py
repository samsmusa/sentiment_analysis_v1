import logging
from functools import lru_cache

from pydantic import BaseSettings, validator

logger = logging.getLogger("uvicorn")


class Settings(BaseSettings):
    APP_ENVIRONMENT: str
    APP_NAME: str
    APP_VERSION: str
    IS_DEBUG: bool
    OPENAPI_URL: str
    SWAGGER_URL: str
    REDOC_URL: str
    API_PREFIX: str | None = "/api/v1"
    OPENAPI_URL: str = "openapi.json"

    @validator("APP_ENVIRONMENT")
    def APP_ENVIRONMENT_must_be_valid(cls, value):
        allowed_statuses = ['development', 'production', 'testing']
        if value not in allowed_statuses:
            raise ValueError(f"APP ENV must be one of: {', '.join(allowed_statuses)}")
        return value

    class Config:
        env_file = './.env'


@lru_cache()
def get_settings() -> BaseSettings:
    logger.info("Loading config settings from the environment...")
    return Settings()
