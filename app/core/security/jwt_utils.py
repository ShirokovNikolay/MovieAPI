from datetime import UTC, datetime, timedelta
from typing import Any

import jwt

from core.config import settings
from core.constants import ACCESS_TOKEN_TYPE, REFRESH_TOKEN_TYPE, TOKEN_TYPE
from schemas.user import UserResponse


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
