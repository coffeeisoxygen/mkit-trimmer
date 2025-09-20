from loguru import logger

from app.custom.exceptions import (
    MemberAlreadyExistsError,
    MemberGenericError,
    MemberNotFoundError,
)
from app.repo.interfaces.intf_member import MemberRepository
from app.schemas.sch_member import (
    MemberCreate,
    MemberInDB,
    MemberUpdate,
)


class MemberCRUDService:
    """service for member CRUD operations."""

    def __init__(self, repository: MemberRepository):
        self.repository = repository

    def get_all_members(self) -> list[MemberInDB]:
        try:
            return self.repository.get_all_members()

        except MemberGenericError as e:
            logger.error(f"Failed to get all members: {e}")
            raise MemberNotFoundError(message="Failed to get all members") from e

    def get_member_by_id(self, member_id: int) -> MemberInDB:
        try:
            member = self.repository.get_member_by_id(member_id)
            if not member:
                logger.error(f"Member with id {member_id} not found")
                raise MemberNotFoundError(
                    message=f"Member with id {member_id} not found",
                    context={"member_id": member_id},
                )
            else:
                return member

        except MemberGenericError as e:
            logger.error(f"Failed to get member by id {member_id}: {e}")
            raise MemberNotFoundError(
                message=f"Failed to get member by id {member_id}",
                context={"member_id": member_id, "detail": str(e)},
            ) from e

    def get_member_by_username(self, member_username: str) -> list[MemberInDB]:
        try:
            return self.repository.get_member_by_username(member_username)
        except MemberGenericError as e:
            logger.error(f"Failed to get member by username {member_username}: {e}")
            raise MemberNotFoundError(
                message=f"Failed to get member by username {member_username}",
                context={"member_username": member_username, "detail": str(e)},
            ) from e

    def add_member(self, member_data: MemberCreate) -> MemberInDB:
        try:
            existing_members = self.repository.get_member_by_username(
                member_username=member_data.name
            )
            if existing_members:
                logger.error(f"Member with name {member_data.name} already exists")
                raise MemberAlreadyExistsError(
                    message=f"Member with name {member_data.name} already exists",
                    context={"member_name": member_data.name},
                )
            # Dump the member data to dict with JSON serializable fields
            logger.info(f"Adding member {member_data.name}")
            return self.repository.add_member(member_data)

        except MemberGenericError as e:
            logger.error(f"Failed to add member {member_data.name}: {e}")
            raise MemberAlreadyExistsError(
                message=f"Failed to add member with name: {member_data.name}",
                context={"member_name": member_data.name, "detail": str(e)},
            ) from e

    def update_member(
        self, member_id: int, member_data: MemberUpdate
    ) -> MemberInDB | None:
        try:
            self.get_member_by_id(member_id)
            logger.info(f"Updating member {member_id}")
            return self.repository.update_member(member_id, member_data)
        except MemberGenericError as e:
            logger.error(f"Failed to update member {member_id}: {e}")
            raise MemberNotFoundError(
                message=f"Failed to update member {member_id}",
                context={"member_id": member_id, "detail": str(e)},
            ) from e

    def delete_member(self, member_id: int) -> list[int]:
        try:
            self.get_member_by_id(member_id)
            return self.repository.delete_member(member_id)
        except MemberGenericError as e:
            logger.error(f"Failed to delete member {member_id}: {e}")
            raise MemberNotFoundError(
                message=f"Failed to delete member {member_id}",
                context={"member_id": member_id, "detail": str(e)},
            ) from e
