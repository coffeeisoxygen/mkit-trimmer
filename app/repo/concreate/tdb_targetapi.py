"""concrete implementation of target api repository."""

from typing import Any

from app.custom.exceptions import TargetAPIGenericError
from app.repo.interfaces.intf_target import TargetApiRepository
from app.schemas.sch_targetapi import TargetApiCreate, TargetApiINDB, TargetApiUpdate
from loguru import logger
from tinydb import where


class TinyDBTargetApiRepository(TargetApiRepository):
    def __init__(self, db: Any):
        self.db = db
        self.table = self.db.table("targetapis")

    def get_all_target_apis(self) -> list[TargetApiINDB]:
        try:
            targetsapis: Any = self.table.all()
            targetsapi_with_ids = []
            for doc in targetsapis:
                doc_with_id = doc.copy()
                doc_with_id["id"] = doc.doc_id
                targetsapi_with_ids.append(doc_with_id)

            return [TargetApiINDB(**t) for t in targetsapi_with_ids]
        except Exception as e:
            logger.error(f"Error fetching all target APIs: {e}")
            raise TargetAPIGenericError() from e

    def get_target_api_by_id(self, target_api_id: int) -> TargetApiINDB | None:
        try:
            target_doc = self.table.get(doc_id=target_api_id)
            if target_doc:
                target_dict = target_doc.copy()
                target_dict["id"] = target_doc.doc_id
                return TargetApiINDB(**target_dict)
            else:
                return None
        except Exception as e:
            logger.error(f"Error fetching target API by id {target_api_id}: {e}")
            raise TargetAPIGenericError(message="Repository error") from e

    def get_target_api_by_username(self, username: str) -> TargetApiINDB | None:
        try:
            targetapi = self.table.get(where("username") == username)
            if targetapi:
                doc_with_id = targetapi.copy()
                doc_with_id["id"] = targetapi.doc_id
                return TargetApiINDB(**doc_with_id)
            else:
                return None
        except Exception as e:
            logger.error(f"Error fetching target API by username {username}: {e}")
            raise TargetAPIGenericError(message="Repository error") from e

    def create_target_api(self, target_api: TargetApiCreate) -> TargetApiINDB:
        try:
            data = target_api.model_dump(mode="json")
            doc_id = self.table.insert(data)
            return TargetApiINDB(**data, id=doc_id)
        except Exception as e:
            logger.error(f"Error creating target API: {e}")
            raise TargetAPIGenericError() from e

    def update_target_api(
        self, target_api_id: int, target_api: TargetApiUpdate
    ) -> TargetApiINDB:
        try:
            update_data = target_api.model_dump(mode="json", exclude_unset=True)
            self.table.update(update_data, doc_ids=[target_api_id])
            updated_doc = self.table.get(doc_id=target_api_id)
            if updated_doc:
                return TargetApiINDB(**updated_doc)
            else:
                return None  # moved to else block for clarity
        except Exception as e:
            logger.error(f"Error updating target API: {e}")
            raise TargetAPIGenericError(message="Repository error") from e

    def delete_target_api(self, target_api_id: int) -> None:
        try:
            self.table.remove(where("id") == target_api_id)
        except Exception as e:
            logger.error(f"Error deleting target API: {e}")
            raise TargetAPIGenericError()
