from fastapi import (
    APIRouter,
    status,
)

from dependencies.annotations.security import (
    AuthUserByRefreshTokenDep,
    GetLoginDataDep,
)
from dependencies.annotations.services import UserServiceDep
from schemas.auth import (
    ResetPasswordRequest,
    SendConfirmationCodeRequest,
    VerifyRegisterUser,
)
from schemas.token_info import TemporaryTokenInfo, TokenInfo
from schemas.user import (
    UserRegistration,
)

router = APIRouter(
    tags=["Auth"],
    prefix="/auth",
)


@router.post(
    "/register",
    response_model=TemporaryTokenInfo,
    status_code=status.HTTP_200_OK,
)
async def register_user(
    registration_user_data: UserRegistration,
    user_service: UserServiceDep,
) -> TemporaryTokenInfo:
    return await user_service.register_user(registration_user_data)


@router.post("/register/resend-confirmation-code")
async def resend_register_confirmation_code(
    send_confirmation_code_request: SendConfirmationCodeRequest,
    user_service: UserServiceDep,
) -> None:
    await user_service.send_register_confirmation_code(send_confirmation_code_request)


@router.post(
    "/register/verify",
    response_model=TokenInfo,
    status_code=status.HTTP_200_OK,
)
async def register_user(
    verify_register_user_data: VerifyRegisterUser,
    user_service: UserServiceDep,
) -> TokenInfo:
    return await user_service.verify_register_user(verify_register_user_data)


@router.post(
    "/login",
    response_model=TemporaryTokenInfo,
    status_code=status.HTTP_200_OK,
)
async def login_user(
    login_data: GetLoginDataDep,
    user_service: UserServiceDep,
) -> TemporaryTokenInfo:
    return await user_service.authenticate_user(login_data)


@router.post("/reset-password")
async def reset_password(
    reset_password_data: ResetPasswordRequest,
    user_service: UserServiceDep,
) -> None:
    await user_service.reset_password(reset_password_data)


@router.post(
    "/send-confirmation-code",
)
async def send_confirmation_code(
    temporary_token_data: TemporaryTokenInfo,
    user_service: UserServiceDep,
) -> None:
    await user_service.send_confirmation_code(temporary_token_data)


@router.post("/confirm-email")
async def confirm_email(
    temporary_token_data: TemporaryTokenInfo,
    confirmation_code: str,
    user_service: UserServiceDep,
) -> TokenInfo:
    return await user_service.confirm_email(temporary_token_data, confirmation_code)


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
