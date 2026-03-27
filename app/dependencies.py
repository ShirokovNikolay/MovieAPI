from typing import Generator, Annotated

from fastapi import Depends
from sqlalchemy.orm import Session
from database import session_factory
from services import (
    GenreService,
    MovieService,
    ReviewService,
    UserService,
)


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
