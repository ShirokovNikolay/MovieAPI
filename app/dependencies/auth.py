from typing import Annotated

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials

from core.config import settings
from core.constants import ACCESS_TOKEN_TYPE, REFRESH_TOKEN_TYPE
from core.security.jwt_utils import decode_jwt
from core.security.validators import validate_token_payload


def get_current_token_payload(
    credentials: Annotated[
        HTTPAuthorizationCredentials,
        Depends(settings.http_bearer),
    ],
) -> dict:
    token = credentials.credentials
    payload = decode_jwt(
        token=token,
    )
    payload["sub"] = int(payload["sub"])
    return payload


def get_current_user_id_by_access_token_payload(
    payload: Annotated[
        dict,
        Depends(get_current_token_payload),
    ],
) -> int:
    validate_token_payload(
        payload=payload,
        target_token_type=ACCESS_TOKEN_TYPE,
    )
    user_id: int = payload["sub"]
    return user_id


def get_current_user_id_by_refresh_token_payload(
    payload: Annotated[
        dict,
        Depends(get_current_token_payload),
    ],
) -> int:
    validate_token_payload(
        payload=payload,
        target_token_type=REFRESH_TOKEN_TYPE,
    )
    user_id: int = payload["sub"]
    return user_id
