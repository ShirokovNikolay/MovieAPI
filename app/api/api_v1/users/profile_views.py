from fastapi import APIRouter, Depends, status

from dependencies.annotations.cache_services import UserCacheServiceDep
from dependencies.annotations.security import AuthUserByAccessTokenDep
from dependencies.rate_limiter import check_rate_limit_auth
from schemas.user import (
    UserPartialUpdate,
    UserResponse,
    UserUpdate,
)

router = APIRouter(
    prefix="/me",
    dependencies=[
        Depends(check_rate_limit_auth),
    ],
)


@router.get(
    "/",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
)
async def get_current_user_profile(
    current_user_id: AuthUserByAccessTokenDep,
    user_cache_service: UserCacheServiceDep,
) -> UserResponse:
    return await user_cache_service.get_user_by_id(current_user_id)


@router.put(
    "/",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
)
async def update_current_user_profile(
    update_data: UserUpdate,
    current_user_id: AuthUserByAccessTokenDep,
    user_cache_service: UserCacheServiceDep,
) -> UserResponse:
    return await user_cache_service.update_user(current_user_id, update_data)


@router.patch(
    "/",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
)
async def partial_update_current_user_profile(
    update_data: UserPartialUpdate,
    current_user_id: AuthUserByAccessTokenDep,
    user_cache_service: UserCacheServiceDep,
) -> UserResponse:
    return await user_cache_service.partial_update_user(current_user_id, update_data)


@router.delete(
    "/",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_current_user_profile(
    current_user_id: AuthUserByAccessTokenDep,
    user_cache_service: UserCacheServiceDep,
) -> None:
    await user_cache_service.delete_user_by_id(current_user_id)
