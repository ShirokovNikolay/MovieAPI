from typing import Annotated

from fastapi import (
    APIRouter,
    status,
    Depends,
)

from dependencies import get_user_service, get_auth_jwt_token
from schemas.token import TokenInfo
from schemas.user import UserResponse, UserCreate
from services import UserService

router = APIRouter(
    tags=["Auth"],
    prefix="/auth",
)


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def register_user(
    create_user_data: UserCreate,
    user_service: Annotated[UserService, Depends(get_user_service)],
):
    return user_service.create_user(create_user_data)


@router.post(
    "/login",
    response_model=TokenInfo,
    status_code=status.HTTP_200_OK,
)
def login_user(
    token: Annotated[str, Depends(get_auth_jwt_token)],
):
    return TokenInfo(
        access_token=token,
        token_type="Bearer",
    )
