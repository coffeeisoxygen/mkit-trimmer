"""fast api application."""

# ruff: noqa
from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, Request
from loguru import logger

from app.auth import MemberAuthService
from app.config import get_all_settings
from app.config.config import TomlSettings
from app.config.watcher import start_config_watcher, stop_config_watcher
from app.custom.mdw import add_process_time_header
from app.dependencies import get_member_auth_service, verify_ip_allowed

# settings hanya untuk middleware global, dependency settings diinject per request
settings: TomlSettings = get_all_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting up...")
    app.state.config = get_all_settings()
    start_config_watcher(app)
    yield
    app.state.config = None
    stop_config_watcher(app)
    logger.info("Shutting down...")


app = FastAPI(lifespan=lifespan)


@app.middleware("http")
async def process_time_middleware(request: Request, call_next):
    return await add_process_time_header(request, call_next)


# settings reloader
@app.get("/debug/settings", response_model=TomlSettings)
async def debug_app_settings():
    return app.state.config


@app.get("/trim")
async def trim_responses(
    request: Request,
    _: None = Depends(verify_ip_allowed),
    auth_service: MemberAuthService = Depends(get_member_auth_service),
):
    await auth_service.authorize(request)
    return {"message": "Authorized"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app="app.main:app", host="0.0.0.0", port=8000, log_level="info", reload=True
    )
