from fastapi import (
    APIRouter,
    status,
)
from pydantic import EmailStr

from dependencies.annotations.cache_services import UserCacheServiceDep
from dependencies.annotations.security import (
    AuthUserByRefreshTokenDep,
    GetLoginDataDep,
)
from dependencies.annotations.services import UserServiceDep
from schemas.auth import ConfirmEmailRequest
from schemas.token_info import TokenInfo
from schemas.user import (
    UserRegistration,
    UserResponse,
)

router = APIRouter(
    tags=["Auth"],
    prefix="/auth",
)


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
async def register_user(
    registration_user_data: UserRegistration,
    user_service: UserCacheServiceDep,
) -> UserResponse:
    return await user_service.create_user(registration_user_data)


@router.post(
    "/login",
    status_code=status.HTTP_200_OK,
)
async def login_user(
    login_data: GetLoginDataDep,
    user_service: UserServiceDep,
) -> EmailStr:
    return await user_service.authenticate_user(login_data)


@router.post("/confirmation_code")
async def send_confirmation_code(
    email: EmailStr,
    user_service: UserServiceDep,
) -> None:
    await user_service.send_confirmation_code(email)


@router.post("/confirm-email")
async def confirm_email(
    confirm_email_request: ConfirmEmailRequest,
    user_service: UserServiceDep,
) -> TokenInfo:
    return await user_service.confirm_email(confirm_email_request)


@router.post(
    "/refresh",
    response_model=TokenInfo,
    response_model_exclude_unset=True,
    status_code=status.HTTP_200_OK,
)
async def refresh_access_token(
    user_id: AuthUserByRefreshTokenDep,
    user_service: UserServiceDep,
) -> TokenInfo:
    return await user_service.refresh_access_token(user_id)
