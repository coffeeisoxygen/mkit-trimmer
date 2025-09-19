"""endpoint to trim received api responses from other services."""

from fastapi import APIRouter, Request

router = APIRouter()


@router.get("/trim")
async def trim_api_response(request: Request):
    """Trim the API response to only include necessary fields."""
    # TODO : Implements Clean Class bases In Services
    pass
