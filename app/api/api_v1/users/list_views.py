from typing import Annotated

from fastapi import APIRouter, Depends, status

from schemas.user import UserResponseList, UserCreate, UserResponse
from services import UserService
from dependencies.services import get_user_service

router = APIRouter()


@router.get(
    "/",
    response_model=UserResponseList,
    status_code=status.HTTP_200_OK,
)
def get_users(
    user_service: Annotated[UserService, Depends(get_user_service)],
):
    return user_service.get_all_users()


@router.post(
    "/",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_user(
    create_user_data: UserCreate,
    user_service: Annotated[UserService, Depends(get_user_service)],
):
    return user_service.create_user(create_user_data)
