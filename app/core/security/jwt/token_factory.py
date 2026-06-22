from core.config import settings
from core.constants import (
    ACCESS_TOKEN_TYPE,
    BEARER_TOKEN_TYPE,
    RECOVER_TOKEN_TYPE,
    REFRESH_TOKEN_TYPE,
    REGISTRATION_TOKEN_TYPE,
    RESET_PASSWORD_TOKEN_TYPE,
    TOKEN_TYPE_FIELD,
    TWO_FACTOR_TOKEN_TYPE,
)
from core.security.jwt.utils import (
    create_access_token_payload,
    create_recover_token_payload,
    create_refresh_token_payload,
    create_registration_token_payload,
    create_reset_password_token_payload,
    create_two_factor_auth_token_payload,
    encode_jwt,
)
from schemas.token_info import TokenInfo
from schemas.user import UserRegistration, UserResponse


def create_access_token(user: UserResponse) -> str:
    payload = create_access_token_payload(user)
    payload.update(
        {TOKEN_TYPE_FIELD: ACCESS_TOKEN_TYPE},
    )
    return encode_jwt(
        payload,
        expires_minutes=settings.jwt.auth.access_token_expire_minutes,
    )


def create_refresh_token(user: UserResponse) -> str:
    payload = create_refresh_token_payload(user)
    payload.update(
        {TOKEN_TYPE_FIELD: REFRESH_TOKEN_TYPE},
    )
    return encode_jwt(
        payload,
        expires_minutes=settings.jwt.auth.refresh_token_expire_minutes,
    )


def create_auth_token(user: UserResponse) -> TokenInfo:
    access_token = create_access_token(user)
    refresh_token = create_refresh_token(user)
    return TokenInfo(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type=BEARER_TOKEN_TYPE,
    )


def create_registration_token(user: UserRegistration) -> str:
    payload = create_registration_token_payload(user)
    payload.update(
        {TOKEN_TYPE_FIELD: REGISTRATION_TOKEN_TYPE},
    )
    return encode_jwt(
        payload=payload,
        secret_key=settings.jwt.registration.secret_key,
        algorithm=settings.jwt.registration.algorithm,
        expires_minutes=settings.jwt.registration.expire_minutes,
    )


def create_two_factor_auth_token(user: UserResponse) -> str:
    payload = create_two_factor_auth_token_payload(user)
    payload.update(
        {TOKEN_TYPE_FIELD: TWO_FACTOR_TOKEN_TYPE},
    )
    return encode_jwt(
        payload=payload,
        secret_key=settings.jwt.two_factor_auth.secret_key,
        algorithm=settings.jwt.two_factor_auth.algorithm,
        expires_minutes=settings.jwt.two_factor_auth.expire_minutes,
    )


def create_recover_token(user: UserResponse) -> str:
    payload = create_recover_token_payload(user)
    payload.update(
        {TOKEN_TYPE_FIELD: RECOVER_TOKEN_TYPE},
    )
    return encode_jwt(
        payload=payload,
        secret_key=settings.jwt.recover.secret_key,
        algorithm=settings.jwt.recover.algorithm,
        expires_minutes=settings.jwt.recover.expire_minutes,
    )


def create_reset_password_token(user: UserResponse) -> str:
    payload = create_reset_password_token_payload(user)
    payload.update(
        {TOKEN_TYPE_FIELD: RESET_PASSWORD_TOKEN_TYPE},
    )
    return encode_jwt(
        payload=payload,
        secret_key=settings.jwt.reset_password.secret_key,
        algorithm=settings.jwt.reset_password.algorithm,
        expires_minutes=settings.jwt.reset_password.expire_minutes,
    )
