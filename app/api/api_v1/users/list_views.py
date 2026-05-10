from fastapi import APIRouter, Depends, status

from dependencies.annotations.cache_services import UserCacheServiceDep
from dependencies.annotations.validators import PaginationPageDep, PaginationSizeDep
from dependencies.auth import get_admin_by_access_token
from schemas.user import UserResponseList

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
    user_cache_service: UserCacheServiceDep,
    size: PaginationSizeDep = 10,
    page: PaginationPageDep = 1,
) -> UserResponseList:
    return await user_cache_service.get_all_users(size, page)
