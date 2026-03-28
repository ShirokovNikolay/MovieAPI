from typing import Generator, Annotated

from fastapi import (
    Depends,
    HTTPException,
    status,
)
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from core.config import (
    settings,
)
from core.constants import TOKEN_TYPE, ACCESS_TOKEN_TYPE, REFRESH_TOKEN_TYPE
from database import session_factory
from services import (
    GenreService,
    MovieService,
    ReviewService,
    UserService,
)
from core.security import decode_jwt


def get_db() -> Generator:
    try:
        db = session_factory()
        yield db
    finally:
        db.close()


def get_genre_service(
    session: Annotated[
        Session,
        Depends(get_db),
    ],
):
    try:
        genre_service = GenreService(session)
        yield genre_service
    finally:
        """
        Действия после view.
        """


def get_movie_service(
    session: Annotated[
        Session,
        Depends(get_db),
    ],
):
    try:
        movie_service = MovieService(session)
        yield movie_service
    finally:
        """
        Действия после view.
        """


def get_review_service(
    session: Annotated[
        Session,
        Depends(get_db),
    ],
):
    try:
        review_service = ReviewService(session)
        yield review_service
    finally:
        """
        Действия после view.
        """


def get_user_service(
    session: Annotated[
        Session,
        Depends(get_db),
    ],
):
    try:
        user_service = UserService(session)
        yield user_service
    finally:
        """
        Действия после view.
        """


def validate_token_payload(payload: dict, target_token_type: str) -> None:
    if payload[TOKEN_TYPE] != target_token_type:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token type",
        )

    if "sub" not in payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token content",
        )


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
