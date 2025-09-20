"""Member service: auth, rate limit, and member info utilities."""

from fastapi import HTTPException, Request
from loguru import logger
from starlette.status import HTTP_403_FORBIDDEN

from app.database.member import MemberDBManager


class MemberService:
    """Service for member authentication, rate limit, and info."""

    def __init__(self, member_db: MemberDBManager):
        self.member_db = member_db

    def get_member_by_ip(self, ip: str) -> dict | None:
        """Get member by IP address."""
        return self.member_db.get_member_by_ip(ip)

    def get_rate_limit_by_ip(self, ip: str, default: str = "5/minute") -> str:
        """Get rate limit for IP."""
        return self.member_db.get_member_rate_limit(ip) or default

    def is_ip_allowed(self, ip: str) -> bool:
        """Check if IP is allowed."""
        is_allowed = self.member_db.is_member_allowed(ip)
        if is_allowed:
            logger.info(f"Access granted for IP: {ip}")
        else:
            logger.warning(f"Access denied for IP: {ip}")
        return is_allowed

    async def authorize(self, request: Request):
        """Authorize request based on client IP."""
        client_ip = request.client.host if request.client else None
        if not client_ip or not self.is_ip_allowed(client_ip):
            raise HTTPException(
                status_code=HTTP_403_FORBIDDEN,
                detail="Access forbidden: IP not allowed",
            )
        return True
