"""fast api application."""

from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, Request
from loguru import logger

from app.auth import MemberAuthService
from app.config import get_all_settings
from app.config.config import TomlSettings
from app.custom.mdw import add_process_time_header, ip_filter_middleware
from app.dependencies import get_member_auth_service

# settings hanya untuk middleware global, dependency settings diinject per request
settings: TomlSettings = get_all_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting up...")
    yield
    logger.info("Shutting down...")


app = FastAPI(lifespan=lifespan)


@app.middleware("http")
async def process_time_middleware(request: Request, call_next):
    return await add_process_time_header(request, call_next)


@app.middleware("http")
async def ip_filter_middleware_wrapper(request: Request, call_next):
    return await ip_filter_middleware(
        request, call_next, allowed_ips=settings.ip_whitelist.ips
    )


# settings reloader
@app.get("/debug/settings", response_model=TomlSettings)
async def get_settings_endpoint(
    settings: TomlSettings = Depends(get_all_settings),
):
    return settings


@app.get("/trim")
async def trime_responses(
    request: Request,
    auth_service: MemberAuthService = Depends(dependency=get_member_auth_service),
):
    await auth_service.authorize(request)
    return {"message": "Authorized"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app="app.main:app", host="0.0.0.0", port=8000, log_level="info", reload=True
    )
