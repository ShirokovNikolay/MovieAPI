from fastapi import (
    APIRouter,
    status,
)

from dependencies.annotations.security import (
    AuthUserByRefreshTokenDep,
)
from dependencies.annotations.services import AuthServiceDep
from schemas.token_info import TokenInfo

router = APIRouter(
    tags=["Refresh Access Token"],
)


@router.post(
    "/refresh",
    response_model=TokenInfo,
    response_model_exclude_unset=True,
    status_code=status.HTTP_200_OK,
)
async def refresh_access_token(
    user_id: AuthUserByRefreshTokenDep,
    auth_service: AuthServiceDep,
) -> TokenInfo:
    return await auth_service.refresh_access_token(user_id)
