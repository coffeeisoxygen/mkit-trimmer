"""fast api application."""

# ruff: noqa
from contextlib import asynccontextmanager
import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from loguru import logger
from app.config import generate_default_config_file, get_all_settings
from app.config.config import TomlSettings
from app.api import register_routers
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded


settings: TomlSettings = get_all_settings()
limiter = Limiter(key_func=get_remote_address)


@asynccontextmanager
@logger.catch()
async def lifespan(app: FastAPI):
    logger.info("Starting up...")
    app.state.admin = settings.admin
    app.state.members = settings.members
    app.state.digipos = settings.digipos
    yield
    app.state.members = None
    app.state.admin = None
    app.state.digipos = None
    logger.info("Shutting down...")


app = FastAPI(lifespan=lifespan)


def rate_limit_exceeded_handler(request: Request, exc: Exception):
    if isinstance(exc, RateLimitExceeded):
        return _rate_limit_exceeded_handler(request, exc)
    return JSONResponse(
        status_code=500,
        content={"detail": "Unexpected exception type for rate limit handler."},
    )


app.add_exception_handler(RateLimitExceeded, rate_limit_exceeded_handler)

register_routers(app)


if __name__ == "__main__":
    generate_default_config_file()
    uvicorn.run(
        app="app.main:app", host="0.0.0.0", port=8000, log_level="info", reload=True
    )
