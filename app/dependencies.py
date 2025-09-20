"""dependency injection module."""

from typing import Annotated

from fastapi import Depends, Request

from app.config.config import MemberSettings
from app.services.member.srv_member import MemberService


# getter untuk app.state.members
def get_member_list(request: Request) -> list[MemberSettings]:
    return request.app.state.members


ListMembers = Annotated[list[str], Depends(get_member_list)]

# getter untuk MemberService


def get_client_ip(request: Request) -> str | None:
    """Get client IP address from request."""
    return request.client.host if request.client else None


def get_member_service(request: Request) -> MemberService:
    return MemberService(request.app.state.members)
