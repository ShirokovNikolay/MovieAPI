from typing import Annotated

from fastapi import APIRouter
from fastapi import status, Depends

from cache_services import UserCacheService
from dependencies.auth import get_admin_by_access_token
from dependencies.cache_services import get_user_cache_service
from schemas.user import UserResponse

router = APIRouter(
    prefix="/{login}",
    dependencies=[
        Depends(get_admin_by_access_token),
    ],
)


@router.get(
    "/",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
)
async def get_user_by_login(
    login: str,
    user_cache_service: Annotated[
        UserCacheService,
        Depends(get_user_cache_service),
    ],
) -> UserResponse:
    return await user_cache_service.get_user_by_login(login)


@router.delete(
    "/",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_user_by_login(
    login: str,
    user_cache_service: Annotated[
        UserCacheService,
        Depends(get_user_cache_service),
    ],
) -> None:
    await user_cache_service.delete_user_by_login(login)
