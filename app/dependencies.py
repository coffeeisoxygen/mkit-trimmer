"""dependency injection module."""

from app.database.init import init_databases
from app.member_services import MemberService


def get_member_service() -> MemberService:
    """Dependency injector for MemberService."""
    member_db, _ = init_databases()
    return MemberService(member_db=member_db)
