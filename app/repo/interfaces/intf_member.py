from abc import ABC, abstractmethod

from app.schemas.sch_member import MemberCreate, MemberInDB, MemberUpdate


class MemberRepository(ABC):
    @abstractmethod
    def get_all_members(self) -> list[MemberInDB]:
        pass

    @abstractmethod
    def get_member_by_id(self, member_id: int) -> MemberInDB | None:
        pass

    @abstractmethod
    def get_member_by_username(self, member_username: str) -> list[MemberInDB]:
        pass

    @abstractmethod
    def add_member(self, member_data: MemberCreate) -> MemberInDB:
        pass

    @abstractmethod
    def update_member(
        self, member_id: int, member_data: MemberUpdate
    ) -> MemberInDB | None:
        pass

    @abstractmethod
    def delete_member(self, member_id: int) -> list[int]:
        pass
