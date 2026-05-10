from fastapi import APIRouter, Depends, status

from dependencies.annotations.cache_services import UserCacheServiceDep
from dependencies.auth import get_admin_by_access_token
from schemas.user import UserResponse

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
    user_cache_service: UserCacheServiceDep,
) -> UserResponse:
    return await user_cache_service.get_user_by_id(user_id)


@router.delete(
    "/",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_user_by_id(
    user_id: int,
    user_cache_service: UserCacheServiceDep,
) -> None:
    await user_cache_service.delete_user_by_id(user_id)
