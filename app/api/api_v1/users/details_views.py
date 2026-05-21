from fastapi import APIRouter, Depends, status

from dependencies.annotations.cache_services import UserCacheServiceDep
from dependencies.annotations.validators import PaginationPageDep, PaginationSizeDep
from dependencies.auth import get_admin_by_access_token
from dependencies.rate_limiter import check_rate_limit_auth
from schemas.user import UserResponse, UserResponseList

router = APIRouter(
    dependencies=[
        Depends(get_admin_by_access_token),
        Depends(check_rate_limit_auth),
    ],
)


@router.get(
    "/",
    response_model=UserResponseList,
    status_code=status.HTTP_200_OK,
)
async def get_users(
    user_cache_service: UserCacheServiceDep,
    size: PaginationSizeDep = 10,
    page: PaginationPageDep = 1,
) -> UserResponseList:
    return await user_cache_service.get_all_users(size, page)


@router.get(
    "/{user_id}",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
)
async def get_user_by_id(
    user_id: int,
    user_cache_service: UserCacheServiceDep,
) -> UserResponse:
    return await user_cache_service.get_user_by_id(user_id)


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_user_by_id(
    user_id: int,
    user_cache_service: UserCacheServiceDep,
) -> None:
    await user_cache_service.delete_user_by_id(user_id)


@router.get(
    "/login/{login}",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
)
async def get_user_by_login(
    login: str,
    user_cache_service: UserCacheServiceDep,
) -> UserResponse:
    return await user_cache_service.get_user_by_login(login)


@router.delete(
    "/login/{login}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_user_by_login(
    login: str,
    user_cache_service: UserCacheServiceDep,
) -> None:
    await user_cache_service.delete_user_by_login(login)
