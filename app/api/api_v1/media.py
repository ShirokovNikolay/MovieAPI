import httpx
from fastapi import APIRouter, Depends, status
from packages.schemas import PresignUrlCreate, PresignUrlResponse

from dependencies.auth import get_admin_by_access_token

router = APIRouter(
    tags=["Media"],
    prefix="/media",
)


@router.post(
    "/presign-url",
    status_code=status.HTTP_201_CREATED,
    response_model=PresignUrlResponse,
    dependencies=[
        Depends(get_admin_by_access_token),
    ],
)
async def get_presign_url(
    presign_url_create: PresignUrlCreate,
) -> PresignUrlResponse:
    async with httpx.AsyncClient() as client:
        request = await client.post(
            url="http://mediaservice:8000/api/v1/presign-url",
            json=presign_url_create.model_dump(),
        )
        return PresignUrlResponse(**request.json())
