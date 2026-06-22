from fastapi import APIRouter
from starlette import status

from dependencies.annotations.services import AuthServiceDep
from schemas.auth import SendConfirmationCodeRequest, VerifyUserEmail
from schemas.token_info import TemporaryTokenInfo, TokenInfo
from schemas.user import UserRegistration

router = APIRouter(
    prefix="/register",
    tags=["Registration"],
)


@router.post(
    "/",
    response_model=TemporaryTokenInfo,
    status_code=status.HTTP_200_OK,
)
async def register_user(
    registration_user_data: UserRegistration,
    auth_service: AuthServiceDep,
) -> TemporaryTokenInfo:
    return await auth_service.register_user(registration_user_data)


@router.post(
    "/resend-confirmation-code",
    status_code=status.HTTP_200_OK,
)
async def resend_register_confirmation_code(
    send_confirmation_code_request: SendConfirmationCodeRequest,
    auth_service: AuthServiceDep,
) -> None:
    await auth_service.send_register_confirmation_code(send_confirmation_code_request)


@router.post(
    "/verify",
    response_model=TokenInfo,
    status_code=status.HTTP_201_CREATED,
)
async def verify_register_user(
    verify_register_user_data: VerifyUserEmail,
    auth_service: AuthServiceDep,
) -> TokenInfo:
    return await auth_service.verify_register_user(verify_register_user_data)
