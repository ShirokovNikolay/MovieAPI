from fastapi import APIRouter, status, Depends
from typing import Annotated

from cache_services import UserCacheService
from dependencies.auth import get_admin_by_access_token
from dependencies.cache_services import get_user_cache_service
from dependencies.rate_limiter import check_rate_limit_auth
from dependencies.services import get_user_service
from schemas.user import UserUpdate, UserPartialUpdate, UserResponse
from services import UserService

router = APIRouter(
    prefix="/{user_id}",
    dependencies=[
        Depends(get_admin_by_access_token),
    ],
)


@router.get(
    "/",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
)
async def get_user_by_id(
    user_id: int,
    user_cache_service: Annotated[
        UserCacheService,
        Depends(get_user_cache_service),
    ],
):
    return await user_cache_service.get_user_by_id(user_id)


@router.put(
    "/",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
)
async def update_user(
    user_id: int,
    update_data: UserUpdate,
    user_cache_service: Annotated[
        UserCacheService,
        Depends(get_user_cache_service),
    ],
):
    return await user_cache_service.update_user(user_id, update_data)


@router.patch(
    "/",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
)
async def partial_update_user(
    user_id: int,
    update_data: UserPartialUpdate,
    user_cache_service: Annotated[
        UserCacheService,
        Depends(get_user_cache_service),
    ],
):
    return await user_cache_service.partial_update_user(user_id, update_data)


@router.delete(
    "/",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_user_by_id(
    user_id: int,
    user_cache_service: Annotated[
        UserCacheService,
        Depends(get_user_cache_service),
    ],
):
    await user_cache_service.delete_user_by_id(user_id)
