from fastapi import APIRouter
from starlette import status

from dependencies.annotations.security import GetLoginDataDep
from dependencies.annotations.services import AuthServiceDep
from schemas.auth import SendConfirmationCodeRequest, VerifyUserEmail
from schemas.token_info import TemporaryTokenInfo, TokenInfo

router = APIRouter(
    prefix="/login",
    tags=["Login"],
)


@router.post(
    "/",
    response_model=TemporaryTokenInfo,
    status_code=status.HTTP_200_OK,
)
async def login_user(
    login_data: GetLoginDataDep,
    auth_service: AuthServiceDep,
) -> TemporaryTokenInfo:
    return await auth_service.authenticate_user(login_data)


@router.post(
    "/resend-confirmation-code",
    status_code=status.HTTP_200_OK,
)
async def resend_authenticate_confirmation_code(
    send_confirmation_code_request: SendConfirmationCodeRequest,
    auth_service: AuthServiceDep,
) -> None:
    await auth_service.send_authenticate_confirmation_code(
        send_confirmation_code_request,
    )


@router.post(
    "/verify",
    status_code=status.HTTP_200_OK,
    response_model=TokenInfo,
)
async def verify_authenticate_user(
    verify_authenticate_user_data: VerifyUserEmail,
    auth_service: AuthServiceDep,
) -> TokenInfo:
    return await auth_service.verify_authenticate_user(verify_authenticate_user_data)
