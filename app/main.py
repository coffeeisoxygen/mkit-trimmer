"""fast api application."""

from contextlib import asynccontextmanager
from pathlib import Path

import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from loguru import logger

from app.api import register_routers
from app.config import generate_default_config_file, get_all_settings
from app.custom.exceptions import AppExceptionError
from app.db.tiny_db import get_db

settings = get_all_settings()
DB_PATH = Path(settings.database_url)


@asynccontextmanager
@logger.catch()
async def lifespan(app: FastAPI):  # noqa: RUF029
    """Lifespan for application."""
    logger.info("Starting up...")
    logger.info(f"Database path: {DB_PATH}")
    app.state.db = get_db(str(DB_PATH))
    yield

    logger.info("Shutting down...")
    app.state.db.close()
    app.state.db = None


app = FastAPI(lifespan=lifespan)


@app.exception_handler(AppExceptionError)
async def app_exception_handler(  # noqa: D103, RUF029
    request: Request,  # noqa: ARG001
    exc: AppExceptionError,  # noqa: ARG001, RUF100
) -> JSONResponse:
    logger.error(f"Application error: {exc.message}", extra=exc.context)
    return JSONResponse(
        status_code=getattr(exc, "status_code", 400),
        content={
            "error": exc.message,
            "context": getattr(exc, "context", {}),
        },
    )


register_routers(app)


if __name__ == "__main__":
    generate_default_config_file()
    uvicorn.run(
        app="app.main:app", host="0.0.0.0", port=8000, log_level="info", reload=True
    )
