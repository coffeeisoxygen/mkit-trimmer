"""dependency injection module."""

from fastapi import Depends, Request

from app.repo.concreate.tdb_member import TinyDBMemberRepository
from app.services.member.member_crud import MemberCRUDService


def get_client_ip(request: Request) -> str:
    """Get client ip address from request."""
    client_host = request.client.host if request.client else "unknown"
    return client_host


def get_db(request: Request):
    return request.app.state.db


def get_member_repo(db=Depends(get_db)) -> TinyDBMemberRepository:
    return TinyDBMemberRepository(db)


def get_member_service(repo=Depends(get_member_repo)) -> MemberCRUDService:
    return MemberCRUDService(repo)
