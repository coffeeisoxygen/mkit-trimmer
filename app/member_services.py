"""Member service: auth, rate limit, and member info utilities."""

from fastapi import HTTPException, Request
from loguru import logger
from starlette.status import HTTP_403_FORBIDDEN

from app.config.config import MemberAccountSettings


class MemberService:
    """Service for member authentication, rate limit, and info."""

    def __init__(self, member_accounts: list[MemberAccountSettings]):
        self.member_accounts = member_accounts

    def __call__(self, ip: str) -> MemberAccountSettings | None:
        return self.member_by_ip(ip)

    @property
    def member_by_ip(self):
        def getter(ip: str) -> MemberAccountSettings | None:
            for account in self.member_accounts:
                if account.ipaddress == ip:
                    return account
            return None

        return getter

    @property
    def rate_limit_by_ip(self):
        def getter(ip: str, default: str = "5/minute") -> str:
            member = self.member_by_ip(ip)
            return getattr(member, "rate_limiter", default) if member else default

        return getter

    @property
    def is_ip_allowed(self):
        def getter(ip: str) -> bool:
            member = self.member_by_ip(ip)
            if member:
                if member.is_allowed:
                    logger.info(f"Access granted for IP: {ip}")
                    return True
                else:
                    logger.warning(
                        f"Access denied for IP: {ip} - is_allowed flag is False"
                    )
                    return False
            logger.warning(
                f"Access denied for IP: {ip} - IP not found in member accounts"
            )
            return False

        return getter

    async def authorize(self, request: Request):
        client_ip = request.client.host if request.client else None
        if not client_ip or not self.is_ip_allowed(client_ip):
            raise HTTPException(
                status_code=HTTP_403_FORBIDDEN,
                detail="Access forbidden: IP not allowed",
            )
        return True
