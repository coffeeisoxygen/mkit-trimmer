"""fast api application."""

# ruff: noqa
from contextlib import asynccontextmanager
import uvicorn
from fastapi import Depends, FastAPI, Request
from fastapi.responses import JSONResponse
from loguru import logger
from app.config import generate_default_config_file, get_all_settings
from app.config.config import TomlSettings
from app.custom.mdw import add_process_time_header
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from app.dependencies import (
    get_member_service,
)
from app.member_services import MemberService


settings: TomlSettings = get_all_settings()
limiter = Limiter(key_func=get_remote_address)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting up...")
    app.state.config = get_all_settings()
    yield
    app.state.config = None
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


@app.middleware("http")
async def process_time_middleware(request: Request, call_next):
    return await add_process_time_header(request, call_next)


# app.middleware("http")(member_rate_limit_middleware(default_limiter))


# settings reloader
# @app.get("/debug/settings", response_model=TomlSettings)
# @limiter.limit(default_limiter)
# async def debug_app_settings(request: Request):
#     return app.state.config


@app.get("/trim")
# @limiter.limit(default_limiter)
async def trim_responses(
    request: Request,
    member_service: MemberService = Depends(get_member_service),
):
    await member_service.authorize(request)
    return {"message": "Authorized"}


if __name__ == "__main__":
    generate_default_config_file()
    uvicorn.run(
        app="app.main:app", host="0.0.0.0", port=8000, log_level="info", reload=True
    )
