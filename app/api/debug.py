from fastapi import APIRouter, Depends

from app.config.config import MemberSettings
from app.dependencies import MemberService, get_client_ip, get_member_service

router = APIRouter()


@router.get("/members", response_model=list[MemberSettings])
async def list_members(
    member_service: MemberService = Depends(get_member_service),
    client_ip: str = Depends(get_client_ip),
):
    if not member_service.authorize(client_ip):
        return {"error": "Unauthorized", "client_ip": client_ip}
    # Serialisasi member jika perlu
    return [m.model_dump() for m in member_service.members]
