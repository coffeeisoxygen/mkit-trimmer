"""dependency injection module."""

from fastapi import Depends

from app.auth import MemberAuthService
from app.config.config import TomlSettings, get_all_settings


def get_member_auth_service(
    settings: TomlSettings = Depends(get_all_settings),
) -> MemberAuthService:
    # Pass list of MemberAccountSettings, not dict
    return MemberAuthService(member_accounts=settings.member_accounts)
