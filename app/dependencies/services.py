from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database import session_factory
from services import GenreService, MovieService, ReviewService, UserService


async def get_db():
    async with session_factory() as db:
        yield db


async def get_genre_service(
    session: Annotated[
        AsyncSession,
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


async def get_movie_service(
    session: Annotated[
        AsyncSession,
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


async def get_review_service(
    session: Annotated[
        AsyncSession,
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


async def get_user_service(
    session: Annotated[
        AsyncSession,
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
