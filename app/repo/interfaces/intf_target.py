"""abstract class for targetapi interfaces."""

from abc import ABC, abstractmethod

from app.schemas.sch_targetapi import TargetApiCreate, TargetApiINDB, TargetApiUpdate


class TargetApiRepository(ABC):
    @abstractmethod
    def get_all_target_apis(self) -> list[TargetApiINDB]:
        raise NotImplementedError

    @abstractmethod
    def get_target_api_by_username(self, username: str) -> TargetApiINDB | None:
        raise NotImplementedError

    @abstractmethod
    def get_target_api_by_id(self, target_api_id: int) -> TargetApiINDB | None:
        raise NotImplementedError

    @abstractmethod
    def create_target_api(self, target_api: TargetApiCreate) -> TargetApiINDB:
        raise NotImplementedError

    @abstractmethod
    def update_target_api(self, target_api: TargetApiUpdate) -> TargetApiINDB:
        raise NotImplementedError

    @abstractmethod
    def delete_target_api(self, target_api_id: int) -> None:
        raise NotImplementedError
