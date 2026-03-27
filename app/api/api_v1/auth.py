from typing import Annotated

from fastapi import (
    APIRouter,
    status,
    Depends,
)

from dependencies import get_user_service
from schemas.token import TokenInfo
from schemas.user import UserResponse, UserCreate, UserLogin
from security import encode_jwt, create_user_payload
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
    login_data: UserLogin,
    user_service: Annotated[UserService, Depends(get_user_service)],
):
    user = user_service.authenticate_user(login_data)
    token = encode_jwt(
        payload=create_user_payload(user),
    )
    return TokenInfo(
        access_token=token,
        token_type="Bearer",
    )
