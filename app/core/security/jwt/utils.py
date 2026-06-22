from datetime import UTC, datetime, timedelta
from typing import Any

import jwt

from core.config import settings
from core.constants import (
    EMAIL_FIELD,
    LOGIN_FIELD,
)
from schemas.user import UserRegistration, UserResponse


def encode_jwt(
    payload: dict[str, Any],
    secret_key: str = settings.jwt.auth.secret_key,
    algorithm: str = settings.jwt.auth.algorithm,
    expires_minutes: int = settings.jwt.auth.access_token_expire_minutes,
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
    secret_key: str = settings.jwt.auth.secret_key,
    algorithm: str = settings.jwt.auth.algorithm,
) -> dict[str, Any]:
    return jwt.decode(
        token,
        secret_key,
        algorithms=[algorithm],
    )


def create_access_token_payload(user: UserResponse) -> dict[str, str]:
    payload = {
        "sub": str(user.id),
        LOGIN_FIELD: user.login,
        EMAIL_FIELD: user.email,
    }
    return payload


def create_refresh_token_payload(user: UserResponse) -> dict[str, str]:
    payload = {
        "sub": str(user.id),
    }
    return payload


def create_registration_token_payload(
    user: UserRegistration,
) -> dict[str, str]:
    payload = {
        "sub": user.login,
        LOGIN_FIELD: user.login,
        EMAIL_FIELD: user.email,
    }
    return payload


def create_two_factor_auth_token_payload(
    user: UserResponse,
) -> dict[str, str]:
    payload = {
        "sub": str(user.id),
        EMAIL_FIELD: user.email,
    }
    return payload


def create_recover_token_payload(
    user: UserResponse,
) -> dict[str, str]:
    payload = {
        "sub": str(user.id),
        EMAIL_FIELD: user.email,
        LOGIN_FIELD: user.login,
    }
    return payload


def create_reset_password_token_payload(
    user: UserResponse,
) -> dict[str, str]:
    payload = {
        "sub": str(user.id),
        EMAIL_FIELD: user.email,
    }
    return payload
