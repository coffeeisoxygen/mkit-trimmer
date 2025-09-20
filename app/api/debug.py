from fastapi import APIRouter, Depends

from app.dependencies import get_member_service
from app.schemas.sch_member import MemberInDB
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
