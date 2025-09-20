"""dependency injection module."""

from fastapi import Depends, HTTPException, Request

from app.auth import MemberAuthService
from app.config.config import TomlSettings, get_all_settings


def get_member_auth_service(
    settings: TomlSettings = Depends(get_all_settings),
) -> MemberAuthService:
    # Pass list of MemberAccountSettings, not dict
    return MemberAuthService(member_accounts=settings.member_accounts)


def verify_ip_allowed(request: Request):
    allowed_ips = getattr(request.app.state.config, "ip_whitelist", None)
    ips = allowed_ips.ips if allowed_ips else []
    client_ip = request.client.host if request.client else None
    if not client_ip or client_ip not in ips:
        raise HTTPException(status_code=403, detail="Access forbidden: IP not allowed")
