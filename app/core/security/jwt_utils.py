from datetime import UTC, datetime, timedelta
from typing import Any

import jwt
from pydantic import EmailStr

from core.config import settings
from core.constants import (
    ACCESS_TOKEN_TYPE,
    RECOVER_ACCOUNT_TEMPORARY_TOKEN_TYPE,
    REFRESH_TOKEN_TYPE,
    REGISTRATION_TEMPORARY_TOKEN_TYPE,
    RESET_PASSWORD_TEMPORARY_TOKEN_TYPE,
    TOKEN_TYPE,
    TWO_FACTOR_VERIFICATION_TEMPORARY_TOKEN_TYPE,
)
from schemas.user import UserRegistration, UserResponse


def encode_jwt(
    payload: dict[str, Any],
    secret_key: str = settings.auth_jwt.secret_key,
    algorithm: str = settings.auth_jwt.algorithm,
    expires_minutes: int = settings.auth_jwt.access_token_expire_minutes,
) -> str:
    to_encode = payload.copy()
    now = datetime.now(UTC)
    expire = now + timedelta(minutes=expires_minutes)
    to_encode.update(
        iat=now,
        exp=expire,
    )
    return jwt.encode(
        to_encode,
        secret_key,
        algorithm=algorithm,
    )


def decode_jwt(
    token: str,
    secret_key: str = settings.auth_jwt.secret_key,
    algorithm: str = settings.auth_jwt.algorithm,
) -> dict[str, Any]:
    return jwt.decode(
        token,
        secret_key,
        algorithms=[algorithm],
    )


def create_user_payload_for_access_token(user: UserResponse) -> dict[str, str]:
    payload = {
        "sub": str(user.id),
        "login": user.login,
        "email": user.email,
    }
    return payload


def create_user_payload_for_refresh_token(user: UserResponse) -> dict[str, str]:
    payload = {
        "sub": str(user.id),
    }
    return payload


def create_user_payload_for_registration_temporary_token(
    user: UserRegistration,
) -> dict[str, str]:
    payload = {
        "sub": user.login,
        "login": user.login,
        "email": user.email,
    }
    return payload


def create_user_payload_for_two_factor_verification_temporary_token(
    user: UserResponse,
) -> dict[str, str]:
    payload = {
        "sub": str(user.id),
        "email": user.email,
    }
    return payload


def create_user_payload_for_reset_password_temporary_token(
    user: UserResponse,
) -> dict[str, str]:
    payload = {
        "sub": str(user.id),
        "email": user.email,
    }
    return payload


def create_user_payload_for_recover_account_temporary_token(
    email: EmailStr,
) -> dict[str, str]:
    payload = {"email": email}
    return payload


def create_access_token(user: UserResponse) -> str:
    payload = create_user_payload_for_access_token(user)
    payload.update(
        {TOKEN_TYPE: ACCESS_TOKEN_TYPE},
    )
    return encode_jwt(
        payload,
        expires_minutes=settings.auth_jwt.access_token_expire_minutes,
    )


def create_refresh_token(user: UserResponse) -> str:
    payload = create_user_payload_for_refresh_token(user)
    payload.update(
        {TOKEN_TYPE: REFRESH_TOKEN_TYPE},
    )
    return encode_jwt(
        payload,
        expires_minutes=settings.auth_jwt.refresh_token_expire_minutes,
    )


def create_registration_temporary_token(user: UserRegistration) -> str:
    payload = create_user_payload_for_registration_temporary_token(user)
    payload.update(
        {TOKEN_TYPE: REGISTRATION_TEMPORARY_TOKEN_TYPE},
    )
    return encode_jwt(
        payload=payload,
        secret_key=settings.confirmation_code_jwt.secret_key,
        algorithm=settings.confirmation_code_jwt.algorithm,
        expires_minutes=settings.confirmation_code_jwt.temporary_token_registration_expire_minutes,
    )


def create_two_factor_verification_temporary_token(user: UserResponse) -> str:
    payload = create_user_payload_for_two_factor_verification_temporary_token(user)
    payload.update(
        {TOKEN_TYPE: TWO_FACTOR_VERIFICATION_TEMPORARY_TOKEN_TYPE},
    )
    return encode_jwt(
        payload=payload,
        secret_key=settings.confirmation_code_jwt.secret_key,
        algorithm=settings.confirmation_code_jwt.algorithm,
        expires_minutes=settings.confirmation_code_jwt.temporary_token_two_factor_expire_minutes,
    )


def create_recover_account_temporary_token(email: EmailStr) -> str:
    payload = create_user_payload_for_recover_account_temporary_token(email)
    payload.update(
        {TOKEN_TYPE: RECOVER_ACCOUNT_TEMPORARY_TOKEN_TYPE},
    )
    return encode_jwt(
        payload=payload,
        secret_key=settings.confirmation_code_jwt.secret_key,
        algorithm=settings.confirmation_code_jwt.algorithm,
        expires_minutes=settings.confirmation_code_jwt.temporary_token_recover_account_expire_minutes,
    )


def create_reset_password_temporary_token(user: UserResponse) -> str:
    payload = create_user_payload_for_reset_password_temporary_token(user)
    payload.update(
        {TOKEN_TYPE: RESET_PASSWORD_TEMPORARY_TOKEN_TYPE},
    )
    return encode_jwt(
        payload=payload,
        secret_key=settings.confirmation_code_jwt.secret_key,
        algorithm=settings.confirmation_code_jwt.algorithm,
        expires_minutes=settings.confirmation_code_jwt.temporary_token_reset_password_expire_minutes,
    )
