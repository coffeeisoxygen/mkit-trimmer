"""middlewares utilities."""

import time

from fastapi import Request
from fastapi.responses import JSONResponse
from loguru import logger


def get_client_ip(request: Request) -> str | None:
    """Get client IP address from request."""
    return request.client.host if request.client else None


async def add_process_time_header(request: Request, call_next):
    """Middleware to add X-Process-Time header and log process time."""
    client_ip = get_client_ip(request)
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = time.perf_counter() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    logger.info(
        f"Request {request.url.path} processed in {process_time:.4f} seconds from IP: {client_ip}"
    )
    return response


async def ip_filter_middleware(request: Request, call_next, allowed_ips):
    """Middleware to filter requests by allowed IPs."""
    client_ip = get_client_ip(request)
    if not client_ip or client_ip not in allowed_ips:
        logger.warning(f"Access denied for IP: {client_ip}")
        return JSONResponse(
            status_code=403, content={"detail": "Access forbidden: IP not allowed"}
        )
    logger.info(f"Access granted for IP: {client_ip}")
    response = await call_next(request)
    return response
