from typing import Generator, Annotated

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from config import settings
from database import session_factory
from services import (
    GenreService,
    MovieService,
    ReviewService,
    UserService,
)
from security import decode_jwt


def get_db() -> Generator:
    try:
        db = session_factory()
        yield db
    finally:
        db.close()


def get_genre_service(
    session: Annotated[Session, Depends(get_db)],
):
    try:
        genre_service = GenreService(session)
        yield genre_service
    finally:
        """
        Действия после view.
        """


def get_movie_service(
    session: Annotated[Session, Depends(get_db)],
):
    try:
        movie_service = MovieService(session)
        yield movie_service
    finally:
        """
        Действия после view.
        """


def get_review_service(
    session: Annotated[Session, Depends(get_db)],
):
    try:
        review_service = ReviewService(session)
        yield review_service
    finally:
        """
        Действия после view.
        """


def get_user_service(
    session: Annotated[Session, Depends(get_db)],
):
    try:
        user_service = UserService(session)
        yield user_service
    finally:
        """
        Действия после view.
        """


def get_current_token_payload(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(settings.security)],
) -> dict:
    token = credentials.credentials
    payload = decode_jwt(
        token=token,
    )
    return payload


def get_current_user_id(
    payload: Annotated[dict, Depends(get_current_token_payload)],
) -> int:
    user_id: int = payload["sub"]
    return user_id
