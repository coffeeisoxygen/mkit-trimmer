"""dependency injection module."""

from fastapi import Depends

from app.config.config import TomlSettings, get_all_settings
from app.member_services import MemberService


def get_member_service(
    settings: TomlSettings = Depends(get_all_settings),
) -> MemberService:
    return MemberService(member_accounts=settings.member_accounts)
