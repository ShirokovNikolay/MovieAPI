from fastapi import APIRouter
from starlette import status

from dependencies.annotations.services import AuthServiceDep
from schemas.auth import (
    RecoverAccountRequest,
    ResetPasswordRequest,
    SendConfirmationCodeRequest,
    VerifyUserEmail,
)
from schemas.token_info import TemporaryTokenInfo

router = APIRouter(
    prefix="/recover",
    tags=["Recover"],
)


@router.post(
    "/",
    response_model=TemporaryTokenInfo,
    status_code=status.HTTP_200_OK,
)
async def recover_account(
    recover_account_data: RecoverAccountRequest,
    auth_service: AuthServiceDep,
) -> TemporaryTokenInfo:
    return await auth_service.recover_account(recover_account_data)


@router.post("/resend-confirmation-code")
async def resend_recover_account_confirmation_code(
    send_confirmation_code_request: SendConfirmationCodeRequest,
    auth_service: AuthServiceDep,
) -> None:
    return await auth_service.send_recover_account_confirmation_code(
        send_confirmation_code_request,
    )


@router.post("/verify")
async def verify_recover_account(
    verify_recover_account_data: VerifyUserEmail,
    auth_service: AuthServiceDep,
) -> TemporaryTokenInfo:
    return await auth_service.verify_recover_account(verify_recover_account_data)


@router.post("/reset-password")
async def reset_password(
    reset_password_data: ResetPasswordRequest,
    auth_service: AuthServiceDep,
) -> None:
    await auth_service.reset_password(reset_password_data)
