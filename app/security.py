import bcrypt
import jwt

from config import settings


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
) -> str:
    return jwt.encode(
        payload,
        secret_key,
        algorithm=algorithm,
    )


def decode_jwt(
    token,
    secret_key: str = settings.auth_jwt.secret_key,
    algorithm: str = settings.auth_jwt.algorithm,
) -> dict:
    return jwt.decode(
        token,
        secret_key,
        algorithms=[algorithm],
    )
