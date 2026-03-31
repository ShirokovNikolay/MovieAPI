from typing import Annotated

from fastapi import (
    APIRouter,
    status,
    Depends,
)
from fastapi.security import OAuth2PasswordRequestForm

from dependencies.auth import get_user_by_refresh_token
from dependencies.services import get_user_service
from schemas.token import TokenInfo
from schemas.user import (
    UserResponse,
    UserCreate,
    UserLogin,
)
from core.security.jwt_utils import (
    create_access_token,
    create_refresh_token,
)
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
    user_service: Annotated[
        UserService,
        Depends(get_user_service),
    ],
):
    return user_service.create_user(create_user_data)


@router.post(
    "/login",
    response_model=TokenInfo,
    status_code=status.HTTP_200_OK,
)
def login_user(
    oauth2_form: Annotated[OAuth2PasswordRequestForm, Depends()],
    user_service: Annotated[
        UserService,
        Depends(get_user_service),
    ],
):
    login_data = UserLogin(
        login=oauth2_form.username,
        password=oauth2_form.password,
    )
    user = user_service.authenticate_user(login_data)
    access_token = create_access_token(user)
    refresh_token = create_refresh_token(user)
    return TokenInfo(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="Bearer",
    )


@router.post(
    "/refresh",
    response_model=TokenInfo,
    response_model_exclude_unset=True,
    status_code=status.HTTP_200_OK,
)
def refresh_access_token(
    user_id: Annotated[
        int,
        Depends(get_user_by_refresh_token),
    ],
    user_service: Annotated[
        UserService,
        Depends(get_user_service),
    ],
):
    user = user_service.get_user_by_id(user_id)
    access_token = create_access_token(user)
    return TokenInfo(access_token=access_token)
