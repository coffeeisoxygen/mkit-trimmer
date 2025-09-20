"""service for member authentication operations.

Includes:
- Auth based on existence and status of ip_address
- Rate limiting based on member config
"""

from app.custom.exceptions import MemberNotFoundError
from app.services.member.member_crud import MemberCRUDService


class MemberAuthService:
    def __init__(self, member_service: MemberCRUDService):
        self.member_service = member_service

    def is_ip_allowed(self, ip_address: str) -> bool:
        """Check if IP address is allowed (exists and is_active)."""
        try:
            members = self.member_service.get_member_by_username(ip_address)
            for member in members:
                if member.is_active and str(member.ip_address) == ip_address:
                    return True
            return False
        except MemberNotFoundError:
            return False

    def get_member_rate_limit(self, ip_address: str) -> tuple[int, str] | None:
        """Get rate limit config for member by IP address."""
        try:
            members = self.member_service.get_member_by_username(ip_address)
            for member in members:
                if str(member.ip_address) == ip_address:
                    return (member.rate_limit, member.rl_interval)
            return None
        except MemberNotFoundError:
            return None
