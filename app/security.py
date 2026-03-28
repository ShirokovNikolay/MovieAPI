from datetime import datetime, timedelta, timezone

import bcrypt
import jwt
from jwt.exceptions import InvalidTokenError
from fastapi import HTTPException, status
from config import settings
from core.constants import TOKEN_TYPE, ACCESS_TOKEN_TYPE, REFRESH_TOKEN_TYPE
from schemas.user import UserResponse


def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    password_bytes = password.encode()
    return bcrypt.hashpw(password_bytes, salt).decode()


def verify_password(password: str, hashed_password: str) -> bool:
    password_bytes = password.encode()
    hashed_password_bytes = hashed_password.encode()
    return bcrypt.checkpw(password_bytes, hashed_password_bytes)


def encode_jwt(
    payload: dict,
    secret_key: str = settings.auth_jwt.secret_key,
    algorithm: str = settings.auth_jwt.algorithm,
    expires_minutes: int = settings.auth_jwt.access_token_expire_minutes,
) -> str:
    to_encode = payload.copy()
    now = datetime.now(timezone.utc)
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
    token,
    secret_key: str = settings.auth_jwt.secret_key,
    algorithm: str = settings.auth_jwt.algorithm,
) -> dict:
    try:
        return jwt.decode(
            token,
            secret_key,
            algorithms=[algorithm],
        )
    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )


def create_user_payload_for_access_token(user: UserResponse) -> dict:
    payload = {
        "sub": str(user.id),
        "login": user.login,
        "email": user.email,
    }
    return payload


def create_user_payload_for_refresh_token(user: UserResponse) -> dict:
    payload = {
        "sub": str(user.id),
    }
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
