from typing import Annotated

from fastapi import APIRouter, Depends, status
from packages.schemas import PresignUrlCreate, PresignUrlResponse

from core.config import settings
from core.constants import MethodType
from dependencies.auth import get_admin_by_access_token
from dependencies.rate_limiter import check_rate_limit_auth
from dependencies.services import get_http_request_service
from services.http_request import HttpRequestService

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
        Depends(check_rate_limit_auth),
    ],
)
async def get_presign_url(
    presign_url_create: PresignUrlCreate,
    http_request_service: Annotated[
        HttpRequestService,
        Depends(get_http_request_service),
    ],
) -> PresignUrlResponse:
    return await http_request_service.get_schema_from_request(
        url=settings.media_service.create_presign_url_endpoint,
        method=MethodType.post.value,  # type: ignore[arg-type]
        json=presign_url_create.model_dump(),
        response_schema=PresignUrlResponse,  # type: ignore[arg-type]
    )
