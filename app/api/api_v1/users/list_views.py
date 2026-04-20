from typing import Annotated

from fastapi import APIRouter, Depends, Query, status

from cache_services import UserCacheService
from dependencies.auth import get_admin_by_access_token
from dependencies.cache_services import get_user_cache_service
from schemas.user import UserCreate, UserResponse, UserResponseList

router = APIRouter(
    dependencies=[
        Depends(get_admin_by_access_token),
    ],
)


@router.get(
    "/",
    response_model=UserResponseList,
    status_code=status.HTTP_200_OK,
)
async def get_users(
    user_cache_service: Annotated[
        UserCacheService,
        Depends(get_user_cache_service),
    ],
    size: Annotated[
        int,
        Query(ge=1),
    ] = 10,
    page: Annotated[
        int,
        Query(ge=1),
    ] = 1,
) -> UserResponseList:
    return await user_cache_service.get_all_users(size, page)


@router.post(
    "/",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_user(
    create_user_data: UserCreate,
    user_cache_service: Annotated[
        UserCacheService,
        Depends(get_user_cache_service),
    ],
) -> UserResponse:
    return await user_cache_service.create_user(create_user_data)
