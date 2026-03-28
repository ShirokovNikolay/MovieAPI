from typing import Annotated

from fastapi import Depends, status, HTTPException
from fastapi.security import HTTPAuthorizationCredentials

from core.config import settings
from core.constants import ACCESS_TOKEN_TYPE, REFRESH_TOKEN_TYPE
from core.security.jwt_utils import decode_jwt
from core.security.validators import validate_token_payload
from dependencies.services import get_review_service
from schemas.review import ReviewResponseList, ReviewResponse
from services import ReviewService


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


def get_own_reviews(
    current_user_id: Annotated[
        int,
        Depends(get_current_user_id_by_access_token_payload),
    ],
    user_id: int,
    review_service: Annotated[
        ReviewService,
        Depends(get_review_service),
    ],
) -> ReviewResponseList:
    if user_id == current_user_id:
        return review_service.get_user_reviews(user_id)
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="You are not allowed to view this user's reviews",
    )


def get_own_review_about_movie(
    current_user_id: Annotated[
        int,
        Depends(get_current_user_id_by_access_token_payload),
    ],
    user_id: int,
    movie_id: int,
    review_service: Annotated[
        ReviewService,
        Depends(get_review_service),
    ],
) -> ReviewResponse:
    if user_id == current_user_id:
        return review_service.get_user_review_about_movie(user_id, movie_id)
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="You are not allowed to view this user's reviews",
    )
