from typing import Any

from app.custom.exceptions import MemberGenericError
from app.repo.interfaces.intf_member import MemberRepository
from app.schemas.sch_member import MemberCreate, MemberInDB, MemberUpdate
from loguru import logger
from tinydb import where


class TinyDBMemberRepository(MemberRepository):
    def __init__(self, db: Any):
        self.db = db
        self.table = self.db.table("members")

    def get_all_members(self) -> list[MemberInDB]:
        try:
            members = self.table.all()
            members_with_ids = []
            for doc in members:
                doc_with_id = doc.copy()
                doc_with_id["id"] = doc.doc_id
                members_with_ids.append(doc_with_id)

            return [MemberInDB(**m) for m in members_with_ids]
        except Exception as e:
            logger.error(f"TinyDB error getting all members: {e}")
            raise MemberGenericError(message="Repository error") from e

    def get_member_by_id(self, member_id: int) -> MemberInDB | None:
        try:
            member_doc = self.table.get(doc_id=member_id)
            if member_doc:
                member_dict = member_doc.copy()
                member_dict["id"] = member_doc.doc_id
                return MemberInDB(**member_dict)
            else:
                return None
        except Exception as e:
            logger.error(f"TinyDB error getting member by id {member_id}: {e}")
            raise MemberGenericError(message="Repository error") from e

    def get_member_by_username(self, member_username: str) -> list[MemberInDB]:
        try:
            members = self.table.search(where("name") == member_username)
            members_with_ids = []
            for doc in members:
                doc_with_id = doc.copy()
                doc_with_id["id"] = doc.doc_id
                members_with_ids.append(doc_with_id)

            return [MemberInDB(**m) for m in members_with_ids]
        except Exception as e:
            logger.error(
                f"TinyDB error getting member by username {member_username}: {e}"
            )
            raise MemberGenericError(message="Repository error") from e

    def add_member(self, member_data: MemberCreate) -> MemberInDB:
        try:
            # Gunakan mode="json" agar Pydantic menangani konversi
            data = member_data.model_dump(mode="json")
            data["is_active"] = True
            data["rate_limit"] = 1
            data["rl_interval"] = "second"

            doc_id = self.table.insert(data)
            data["id"] = doc_id
            return MemberInDB(**data)
        except Exception as e:
            logger.error(f"TinyDB error adding member {member_data.name}: {e}")
            raise MemberGenericError(message="Repository error") from e

    def update_member(
        self, member_id: int, member_data: MemberUpdate
    ) -> MemberInDB | None:
        try:
            update_data = member_data.model_dump(mode="json", exclude_unset=True)
            self.table.update(update_data, doc_ids=[member_id])

            member_doc = self.table.get(doc_id=member_id)
            if member_doc:
                member_dict = member_doc.copy()
                member_dict["id"] = member_doc.doc_id
                return MemberInDB(**member_dict)
            return None
        except Exception as e:
            logger.error(f"TinyDB error updating member {member_id}: {e}")
            raise MemberGenericError(message="Repository error") from e

    def delete_member(self, member_id: int) -> list[int]:
        try:
            return self.table.remove(doc_ids=[member_id])
        except Exception as e:
            logger.error(f"TinyDB error deleting member {member_id}: {e}")
            raise MemberGenericError(message="Repository error") from e
