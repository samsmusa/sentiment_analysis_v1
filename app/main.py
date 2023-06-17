import logging
import os
import time

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from core.config import DevelopmentConfig, ProductionConfig, TestConfig
from core.config_mysql import get_mysql_engine
from core.config_neo4j import init_driver
from core.event_handlers import start_app_handler, stop_app_handler
from core.log_middleware import RouterLoggingMiddleware


def get_app(test_config=None) -> FastAPI:
    settings = load_config(test_config)
    fast_app = FastAPI(
        servers=[
            {"url": "/", "description": "localhost"},
            {
                "url": "http://ai.shared.local",
                "description": "ai.shared.local",
            },
        ],
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        debug=settings.IS_DEBUG,
    )

    fast_app.state.config = settings
    fast_app.mount("/static", StaticFiles(directory="static"), name="static")
    origins = ["http://localhost:3000", "http://localhost:8000", "*"]

    fast_app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=True, allow_methods=["*"],
                            allow_headers=["*"], )

    fast_app.add_event_handler("startup", start_app_handler(fast_app))
    fast_app.add_event_handler("shutdown", stop_app_handler())
    fast_app.state.mysql_engine = get_mysql_engine(fast_app.state.config)

    init_driver(fast_app)
    setup_routes(fast_app)
    return fast_app


def setup_redis(fast_app):
    """Set up a Redis client."""
    # app.redis = Redis(
    #     host=app.config["REDIS_HOST"],
    #     port=app.config["REDIS_PORT"],
    #     db=app.config["REDIS_DB"],
    # )
    pass


def setup_routes(fast_app: FastAPI):
    """Register routes."""

    fast_app.include_router(api_router, prefix=fast_app.state.config.API_PREFIX)


def load_config(test_config):
    """
    Load the configuration from the environment
    """
    env = os.getenv("APP_ENVIRONMENT", "development")
    if test_config is not None:
        env = test_config['env']
    if env == "development":
        return DevelopmentConfig()
    elif env == "production":
        return ProductionConfig()
    elif env == "testing":
        return TestConfig()
    else:
        raise ValueError(f"Invalid APP_ENVIRONMENT value: {env}")


app = get_app()


@app.middleware("http")
async def add_process_time_header(request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(f'{process_time:0.4f} sec')
    return response


logger = logging.getLogger(__name__)
app.add_middleware(RouterLoggingMiddleware, logger=logger)


@app.get('/')
def startup():
    return 'hellow world'
