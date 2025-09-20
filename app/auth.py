"""authorize member access based on IP and is_allowed flag."""

from fastapi import HTTPException, Request
from loguru import logger
from starlette.status import HTTP_403_FORBIDDEN

from app.config.config import MemberAccountSettings


class MemberAuthService:
    """Service to authorize member access based on IP and is_allowed flag."""

    def __init__(self, member_accounts: list[MemberAccountSettings]):
        self.member_accounts = member_accounts

    def is_ip_allowed(self, ip: str) -> bool:
        """Check if the given IP address is allowed."""
        for account in self.member_accounts:
            if account.ipaddress == ip:
                if account.is_allowed:
                    logger.info(f"Access granted for IP: {ip}")
                    return True
                else:
                    logger.warning(
                        f"Access denied for IP: {ip} - is_allowed flag is False"
                    )
                    return False
        logger.warning(f"Access denied for IP: {ip} - IP not found in member accounts")
        return False

    async def authorize(self, request: Request):
        """Authorize the request based on client IP."""
        client_ip = request.client.host if request.client else None
        if not client_ip or not self.is_ip_allowed(client_ip):
            raise HTTPException(
                status_code=HTTP_403_FORBIDDEN,
                detail="Access forbidden: IP not allowed",
            )
        return True
