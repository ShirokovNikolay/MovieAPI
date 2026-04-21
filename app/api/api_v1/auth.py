from fastapi import (
    APIRouter,
    status,
)

from core.constants import BEARER_TOKEN_TYPE
from core.security.jwt_utils import (
    create_access_token,
    create_refresh_token,
)
from dependencies.annotations.cache_services import UserCacheServiceDep
from dependencies.annotations.security import (
    AuthUserByRefreshTokenDep,
    OAuth2Dep,
)
from schemas.token import TokenInfo
from schemas.user import (
    UserCreate,
    UserLogin,
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
    create_user_data: UserCreate,
    user_service: UserCacheServiceDep,
) -> UserResponse:
    return await user_service.create_user(create_user_data)


@router.post(
    "/login",
    response_model=TokenInfo,
    status_code=status.HTTP_200_OK,
)
async def login_user(
    oauth2_form: OAuth2Dep,
    user_service: UserCacheServiceDep,
) -> TokenInfo:
    login_data = UserLogin(
        login=oauth2_form.username,
        password=oauth2_form.password,
    )
    user = await user_service.authenticate_user(login_data)
    access_token = create_access_token(user)
    refresh_token = create_refresh_token(user)
    return TokenInfo(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type=BEARER_TOKEN_TYPE,
    )


@router.post(
    "/refresh",
    response_model=TokenInfo,
    response_model_exclude_unset=True,
    status_code=status.HTTP_200_OK,
)
async def refresh_access_token(
    user_id: AuthUserByRefreshTokenDep,
    user_service: UserCacheServiceDep,
) -> TokenInfo:
    user = await user_service.get_user_by_id(user_id)
    access_token = create_access_token(user)
    return TokenInfo(access_token=access_token)
