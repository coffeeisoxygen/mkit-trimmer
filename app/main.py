"""fast api application."""

from fastapi import FastAPI, Request

from app.config import get_all_settings
from app.config.config import TomlSettings
from app.custom.mdw import add_process_time_header, ip_filter_middleware

settings: TomlSettings = get_all_settings()
app = FastAPI()


@app.middleware("http")
async def process_time_middleware(request: Request, call_next):
    return await add_process_time_header(request, call_next)


@app.middleware("http")
async def ip_filter_middleware_wrapper(request: Request, call_next):
    return await ip_filter_middleware(
        request, call_next, allowed_ips=settings.ip_whitelist.ips
    )


@app.get("/")
async def root():
    """Root endpoint."""
    return {"message": "Hello World"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app="app.main:app", host="0.0.0.0", port=8000, log_level="info", reload=True
    )
