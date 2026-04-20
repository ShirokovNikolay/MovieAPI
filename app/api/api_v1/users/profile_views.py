from typing import Annotated

from fastapi import APIRouter, Depends, status

from cache_services import UserCacheService
from dependencies.auth import get_user_by_access_token
from dependencies.cache_services import get_user_cache_service
from schemas.user import (
    UserPartialUpdate,
    UserResponse,
    UserUpdate,
)

router = APIRouter(
    prefix="/me",
)


@router.get(
    "/",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
)
async def get_user_profile(
    current_user_id: Annotated[
        int,
        Depends(get_user_by_access_token),
    ],
    user_cache_service: Annotated[
        UserCacheService,
        Depends(get_user_cache_service),
    ],
) -> UserResponse:
    return await user_cache_service.get_user_by_id(current_user_id)


@router.put(
    "/",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
)
async def update_user_profile(
    update_data: UserUpdate,
    current_user_id: Annotated[
        int,
        Depends(get_user_by_access_token),
    ],
    user_cache_service: Annotated[
        UserCacheService,
        Depends(get_user_cache_service),
    ],
) -> UserResponse:
    return await user_cache_service.update_user(current_user_id, update_data)


@router.patch(
    "/",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
)
async def partial_update_user_profile(
    update_data: UserPartialUpdate,
    current_user_id: Annotated[
        int,
        Depends(get_user_by_access_token),
    ],
    user_cache_service: Annotated[
        UserCacheService,
        Depends(get_user_cache_service),
    ],
) -> UserResponse:
    return await user_cache_service.partial_update_user(current_user_id, update_data)


@router.delete(
    "/",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_user_profile(
    current_user_id: Annotated[
        int,
        Depends(get_user_by_access_token),
    ],
    user_cache_service: Annotated[
        UserCacheService,
        Depends(get_user_cache_service),
    ],
) -> None:
    await user_cache_service.delete_user_by_id(current_user_id)
