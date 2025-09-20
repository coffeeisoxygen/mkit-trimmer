"""Member database manager."""

from typing import Any

from loguru import logger

from app.database.base import BaseDBManager


class MemberDBManager(BaseDBManager):
    """Database manager for member accounts."""

    def __init__(self, db_path: str, table_name: str = "members"):
        super().__init__(db_path, table_name)

    def get_member_by_ip(self, ipaddress: str) -> dict[str, Any] | None:
        """Get member by IP address."""
        result = self.search(self.query.ipaddress == ipaddress)
        return result[0] if result else None

    def get_member_by_name(self, name: str) -> dict[str, Any] | None:
        """Get member by name."""
        result = self.search(self.query.name == name)
        return result[0] if result else None

    def create_member(
        self,
        name: str,
        ipaddress: str,
        report_url: str,
        is_allowed: bool = True,
        rate_limiter: str = "1/minute",
    ) -> int:
        """Create a new member account."""
        # Check if member already exists
        existing = self.get_member_by_ip(ipaddress)
        if existing:
            raise ValueError(f"Member with IP {ipaddress} already exists")

        member_data = {
            "name": name,
            "ipaddress": ipaddress,
            "report_url": report_url,
            "is_allowed": is_allowed,
            "rate_limiter": rate_limiter,
        }

        doc_id = self.insert(member_data)
        logger.info(f"Created member: {name} ({ipaddress})")
        return doc_id

    def update_member_status(self, ipaddress: str, is_allowed: bool) -> bool:
        """Update member allowed status."""
        member = self.get_member_by_ip(ipaddress)
        if not member:
            return False
        doc_id = member.get("_doc_id") if member and "_doc_id" in member else None
        if not doc_id:
            return False
        return self.update(doc_id, {"is_allowed": is_allowed})

    def is_member_allowed(self, ipaddress: str) -> bool:
        """Check if member is allowed."""
        member = self.get_member_by_ip(ipaddress)
        return member.get("is_allowed", False) if member else False

    def get_member_rate_limit(self, ipaddress: str) -> str:
        """Get member rate limit."""
        member = self.get_member_by_ip(ipaddress)
        return member.get("rate_limiter", "1/minute") if member else "1/minute"
