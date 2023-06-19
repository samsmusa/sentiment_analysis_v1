import logging
import time

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.core.config import get_settings
from app.core.event_handlers import start_app_handler, stop_app_handler
from app.routers.router import api

templates = Jinja2Templates(directory="app/templates")


def get_app(test_config=None) -> FastAPI:
    settings = get_settings()
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

    fast_app.mount("/static", StaticFiles(directory="app/static"), name="static")
    origins = ["http://localhost:3000", "http://localhost:8000", "*"]

    fast_app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=True, allow_methods=["*"],
                            allow_headers=["*"], )

    fast_app.add_event_handler("startup", start_app_handler(fast_app))
    fast_app.add_event_handler("shutdown", stop_app_handler())
    setup_routes(fast_app)
    return fast_app


def setup_routes(fast_app: FastAPI):
    """Register routes."""
    settings = get_settings()
    fast_app.include_router(api, prefix=settings.API_PREFIX)


app = get_app()


@app.middleware("http")
async def add_process_time_header(request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(f'{process_time:0.4f} sec')
    return response


logger = logging.getLogger(__name__)



@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse("home/index.html", {"request": request})
