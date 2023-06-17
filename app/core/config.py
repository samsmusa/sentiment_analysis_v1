import os

from pydantic import BaseSettings, validator


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
    DOCS_URL: str = "docs"
    REDOC_URL: str = "redocs"
    DEBUG: bool = False
    TESTING: bool = False
    PRODUCTION: bool = False
    BASE_DIR: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # REDIS_HOST: str
    # REDIS_PORT: int
    # REDIS_DB: int
    VERSION: str = 1.2
    SECRET_KEY: str
    JWT_PUBLIC_KEY: str
    JWT_PRIVATE_KEY: str
    REFRESH_TOKEN_EXPIRES_IN: int
    ACCESS_TOKEN_EXPIRES_IN: int
    JWT_ALGORITHM: str
    CLIENT_ORIGIN: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    TOKEN_HEADER: str
    TOKEN_URL: str
    CRYPTO_SCHEMA: str
    MYSQL_DATABASE_HOSTNAME: str
    MYSQL_DATABASE_USERNAME: str
    MYSQL_DATABASE_PASSWORD: str
    MYSQL_DATABASE_NAME: str
    NEO4J_URI: str
    NEO4J_USERNAME: str
    NEO4J_PASSWORD: str
    KNN_PATH: str
    TFIDF_PATH: str
    MODEL_PATH: str
    KEYCLOAK_PUBLIC: str

    @validator("APP_ENVIRONMENT")
    def APP_ENVIRONMENT_must_be_valid(cls, value):
        allowed_statuses = ['development', 'production', 'testing']
        if value not in allowed_statuses:
            raise ValueError(f"APP ENV must be one of: {', '.join(allowed_statuses)}")
        return value

    class Config:
        env_file = './.env'


class DevelopmentConfig(Settings):
    """Development configuration."""

    DEBUG: bool = True
    TESTING: bool = True
    PRODUCTION: bool = False


class TestConfig(Settings):
    """Test configuration."""

    DEBUG: bool = True
    TESTING: bool = True
    PRODUCTION: bool = False


class ProductionConfig(Settings):
    """Production configuration."""

    DEBUG: bool = False
    TESTING: bool = False
    PRODUCTION: bool = True


settings = Settings()
