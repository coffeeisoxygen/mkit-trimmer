"""middlewares utilities."""

# ruff : noqa
import time

from fastapi import Request
from loguru import logger
from starlette.responses import JSONResponse as StarletteJSONResponse

from app.dependencies import MemberService


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


# Custom rate limiter middleware per member (factory)
rate_limit_storage = {}


def member_rate_limit_middleware(default_limit: str = "5/minute"):
    async def middleware(request: Request, call_next):
        config = getattr(request.app.state, "config", None)
        member_accounts = getattr(config, "member_accounts", [])
        member_service = MemberService(member_accounts)
        ip = get_client_ip(request)
        limit_str = (
            member_service.rate_limit_by_ip(ip, default=default_limit)
            if ip
            else default_limit
        )
        # Parse limit string (contoh: "5/minute")
        try:
            max_req, per = limit_str.split("/")
            max_req = int(max_req)
            per_seconds = 60 if per == "minute" else 1
        except Exception:
            max_req = 5
            per = "minute"  # default value for per
            per_seconds = 60
        now = int(time.time())
        window = now // per_seconds
        key = f"{ip}:{window}"
        count = rate_limit_storage.get(key, 0)

        if count >= max_req:
            reset_time = (window + 1) * per_seconds
            reset_dt = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(reset_time))
            logger.warning(
                f"Rate limit exceeded for IP {ip}. Limit: {max_req}/{per}. Try again after {reset_dt}"
            )
            return StarletteJSONResponse(
                status_code=429,
                content={
                    "detail": "Rate limit exceeded",
                    "limit": f"{max_req}/{per}",
                    "ip": ip,
                    "reset_time": reset_dt,
                },
            )
        rate_limit_storage[key] = count + 1
        return await call_next(request)

    return middleware
