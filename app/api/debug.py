from fastapi import APIRouter, Depends

from app.dependencies import get_member_service
from app.schemas.sch_member import MemberCreate, MemberInDB, MemberUpdate
from app.services.member.member_crud import MemberCRUDService

router = APIRouter()


@router.get("/members", response_model=list[MemberInDB])
def get_members(service: MemberCRUDService = Depends(get_member_service)):
    return service.get_all_members()


@router.get("/members/{member_id}", response_model=MemberInDB)
def get_member(
    member_id: int, service: MemberCRUDService = Depends(get_member_service)
):
    return service.get_member_by_id(member_id)


@router.post("/members", response_model=MemberInDB, status_code=201)
def create_member(
    member_data: MemberCreate,
    service: MemberCRUDService = Depends(get_member_service),
):
    return service.add_member(member_data)


@router.put("/members/{member_id}", response_model=MemberInDB)
def update_member(
    member_id: int,
    member_data: MemberUpdate,
    service: MemberCRUDService = Depends(get_member_service),
):
    """Update an existing member by ID.

    Args:
        member_id (int): The ID of the member to update.
        member_data (MemberUpdate): The updated member data.
        service (MemberCRUDService): The member CRUD service.

    Returns:
        MemberInDB: The updated member.
    """
    return service.update_member(member_id, member_data)


@router.delete("/members/{member_id}", response_model=int)
def delete_member(
    member_id: int, service: MemberCRUDService = Depends(get_member_service)
):
    deleted_ids = service.delete_member(member_id)
    return deleted_ids[0] if deleted_ids else None
