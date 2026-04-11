from typing import Annotated

from fastapi import APIRouter, Depends, status, Query

from dependencies.auth import get_admin_by_access_token
from schemas.user import UserResponseList, UserCreate, UserResponse
from services import UserService
from dependencies.services import get_user_service

router = APIRouter(
    dependencies=[Depends(get_admin_by_access_token)],
)


@router.get(
    "/",
    response_model=UserResponseList,
    status_code=status.HTTP_200_OK,
)
async def get_users(
    user_service: Annotated[UserService, Depends(get_user_service)],
    size: int = Query(10, ge=1),
    page: int = Query(1, ge=1),
):
    return await user_service.get_all_users(size, page)


@router.post(
    "/",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_user(
    create_user_data: UserCreate,
    user_service: Annotated[UserService, Depends(get_user_service)],
):
    return await user_service.create_user(create_user_data)
