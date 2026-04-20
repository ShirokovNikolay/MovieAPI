from typing import Annotated

from fastapi import APIRouter, Depends, status

from cache_services import UserCacheService
from dependencies.auth import get_admin_by_access_token
from dependencies.cache_services import get_user_cache_service
from schemas.user import UserPartialUpdate, UserResponse, UserUpdate

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
) -> UserResponse:
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
) -> UserResponse:
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
) -> UserResponse:
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
) -> None:
    await user_cache_service.delete_user_by_id(user_id)
