from pydantic import EmailStr

from core.config import settings
from core.constants import (
    ACCESS_TOKEN_TYPE,
    RECOVER_TOKEN_TYPE,
    REFRESH_TOKEN_TYPE,
    REGISTRATION_TOKEN_TYPE,
    RESET_PASSWORD_TOKEN_TYPE,
    TOKEN_TYPE_FIELD,
    TWO_FACTOR_TOKEN_TYPE,
)
from core.security.jwt_utils.token_factory_utils import (
    create_access_token_payload,
    create_recover_token_payload,
    create_refresh_token_payload,
    create_registration_token_payload,
    create_reset_password_token_payload,
    create_two_factor_token_payload,
    encode_jwt,
)
from schemas.user import UserRegistration, UserResponse


def create_access_token(user: UserResponse) -> str:
    payload = create_access_token_payload(user)
    payload.update(
        {TOKEN_TYPE_FIELD: ACCESS_TOKEN_TYPE},
    )
    return encode_jwt(
        payload,
        expires_minutes=settings.auth_jwt.access_token_expire_minutes,
    )


def create_refresh_token(user: UserResponse) -> str:
    payload = create_refresh_token_payload(user)
    payload.update(
        {TOKEN_TYPE_FIELD: REFRESH_TOKEN_TYPE},
    )
    return encode_jwt(
        payload,
        expires_minutes=settings.auth_jwt.refresh_token_expire_minutes,
    )


def create_registration_token(user: UserRegistration) -> str:
    payload = create_registration_token_payload(user)
    payload.update(
        {TOKEN_TYPE_FIELD: REGISTRATION_TOKEN_TYPE},
    )
    return encode_jwt(
        payload=payload,
        secret_key=settings.confirmation_code_jwt.secret_key,
        algorithm=settings.confirmation_code_jwt.algorithm,
        expires_minutes=settings.confirmation_code_jwt.registration_token_expire_minutes,
    )


def create_two_factor_token(user: UserResponse) -> str:
    payload = create_two_factor_token_payload(user)
    payload.update(
        {TOKEN_TYPE_FIELD: TWO_FACTOR_TOKEN_TYPE},
    )
    return encode_jwt(
        payload=payload,
        secret_key=settings.confirmation_code_jwt.secret_key,
        algorithm=settings.confirmation_code_jwt.algorithm,
        expires_minutes=settings.confirmation_code_jwt.two_factor_token_expire_minutes,
    )


def create_recover_token(email: EmailStr) -> str:
    payload = create_recover_token_payload(email)
    payload.update(
        {TOKEN_TYPE_FIELD: RECOVER_TOKEN_TYPE},
    )
    return encode_jwt(
        payload=payload,
        secret_key=settings.confirmation_code_jwt.secret_key,
        algorithm=settings.confirmation_code_jwt.algorithm,
        expires_minutes=settings.confirmation_code_jwt.recover_token_expire_minutes,
    )


def create_reset_password_token(user: UserResponse) -> str:
    payload = create_reset_password_token_payload(user)
    payload.update(
        {TOKEN_TYPE_FIELD: RESET_PASSWORD_TOKEN_TYPE},
    )
    return encode_jwt(
        payload=payload,
        secret_key=settings.confirmation_code_jwt.secret_key,
        algorithm=settings.confirmation_code_jwt.algorithm,
        expires_minutes=settings.confirmation_code_jwt.reset_password_token_expire_minutes,
    )
