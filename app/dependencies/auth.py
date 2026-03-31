from typing import Annotated

from fastapi import Depends, status, HTTPException

from core.config import settings
from core.constants import ACCESS_TOKEN_TYPE, REFRESH_TOKEN_TYPE
from core.security.jwt_utils import decode_jwt
from core.security.validators import validate_token_payload
from dependencies.services import get_user_service
from services import UserService


def get_token_payload(
    token: Annotated[
        str,
        Depends(settings.oauth2_scheme),
    ],
) -> dict:
    payload = decode_jwt(token=token)
    payload["sub"] = int(payload["sub"])
    return payload


def get_user_by_access_token(
    payload: Annotated[
        dict,
        Depends(get_token_payload),
    ],
) -> int:
    validate_token_payload(
        payload=payload,
        target_token_type=ACCESS_TOKEN_TYPE,
    )
    user_id: int = payload["sub"]
    return user_id


def get_user_by_refresh_token(
    payload: Annotated[
        dict,
        Depends(get_token_payload),
    ],
) -> int:
    validate_token_payload(
        payload=payload,
        target_token_type=REFRESH_TOKEN_TYPE,
    )
    user_id: int = payload["sub"]
    return user_id


async def get_admin_by_access_token(
    user_id: Annotated[
        int,
        Depends(get_user_by_access_token),
    ],
    user_service: Annotated[
        UserService,
        Depends(get_user_service),
    ],
) -> int:
    if await user_service.is_admin(user_id):
        return user_id
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="You are not allowed to access this resource",
    )
