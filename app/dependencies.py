"""dependency injection module."""

from fastapi import Depends, Request

from app.repo.concreate.tdb_member import TinyDBMemberRepository
from app.services.member.member_crud import MemberCRUDService


def get_client_ip(request: Request) -> str:
    """Get client ip address from request."""
    client_host = request.client.host if request.client else "unknown"
    return client_host


def get_db(request: Request) -> object:
    """Get the database instance from the FastAPI app state.

    Args:
        request (Request): The current request object.

    Returns:
        object: The database instance.
    """
    return request.app.state.db


def get_member_repo(db: object = Depends(get_db)) -> TinyDBMemberRepository:
    """Dependency to provide TinyDBMemberRepository.

    Args:
        db (object): The database instance.

    Returns:
        TinyDBMemberRepository: The member repository.
    """
    return TinyDBMemberRepository(db)


def get_member_service(
    repo: TinyDBMemberRepository = Depends(get_member_repo),
) -> MemberCRUDService:
    """Dependency to provide MemberCRUDService.

    Args:
        repo (TinyDBMemberRepository): The member repository.

    Returns:
        MemberCRUDService: The member CRUD service.
    """
    return MemberCRUDService(repo)
