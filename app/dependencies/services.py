from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database.connection import session_factory
from redis_client import RedisClient
from services import GenreService, MovieService, ReviewService, UserService
from services.favorite_movie import FavoriteMovieService
from services.watch_history import WatchHistoryService


async def get_db():
    async with session_factory() as db:
        yield db


async def get_redis_client():
    async with RedisClient() as redis_client:
        yield redis_client


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


async def get_favorite_movie_service(
    session: Annotated[
        AsyncSession,
        Depends(get_db),
    ],
):
    try:
        favorite_movie_service = FavoriteMovieService(session)
        yield favorite_movie_service
    finally:
        """
        Действия после view.
        """


async def get_watch_history_service(
    session: Annotated[
        AsyncSession,
        Depends(get_db),
    ],
):
    try:
        watch_history_service = WatchHistoryService(session)
        yield watch_history_service
    finally:
        """
        Действия после view.
        """
