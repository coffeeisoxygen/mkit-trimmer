"""Member service.

member di autorisasi jika ip addressnya terdaftar di config.toml
dsini juga akan handle rate limiter per member
jika bukan member, maka tidak di izinkan mengakses endpoint trim
"""

from loguru import logger


class MemberService:
    def __init__(self, members: list):
        self.members = members

    def authorize(self, ip: str) -> bool:
        """Authorize member by IP address.

        Returns True jika ip ditemukan dan is_allowed True, selain itu False.
        """
        member = next((m for m in self.members if m.ipaddress == ip), None)
        if not member:
            logger.bind(ip=ip).warning("IP not found in member list")
            return False
        if not member.is_allowed:
            logger.bind(ip=ip, name=getattr(member, "name", None)).warning(
                "Member found but not allowed"
            )
            return False
        logger.bind(ip=ip, name=getattr(member, "name", None)).info("Member authorized")
        return True
