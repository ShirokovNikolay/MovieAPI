from collections.abc import AsyncGenerator
from typing import Annotated

from fastapi import Depends
from httpx import AsyncClient
from packages.rabbitmq import RabbitMQService, get_rabbitmq_service
from sqlalchemy.ext.asyncio import AsyncSession

from core.database.connection import session_factory
from core.redis import CacheService
from dependencies.caching import get_cache_service_for_confirmation_codes
from services import GenreService, MovieService, ReviewService, UserService
from services.favorite_movie import FavoriteMovieService
from services.http_request import HttpRequestService
from services.watch_history import WatchHistoryService


async def get_http_request_client() -> AsyncGenerator[AsyncClient]:
    async with AsyncClient() as client:
        yield client


async def get_http_request_service(
    http_request_client: Annotated[
        AsyncClient,
        Depends(get_http_request_client),
    ],
) -> AsyncGenerator[HttpRequestService]:
    http_request_service = HttpRequestService(
        http_request_client=http_request_client,
    )
    yield http_request_service


async def get_db() -> AsyncGenerator[AsyncSession]:
    async with session_factory() as db:
        yield db


async def get_genre_service(
    session: Annotated[
        AsyncSession,
        Depends(get_db),
    ],
    rabbitmq_service: Annotated[
        RabbitMQService,
        Depends(get_rabbitmq_service),
    ],
) -> AsyncGenerator[GenreService]:
    try:
        genre_service = GenreService(session, rabbitmq_service)
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
    rabbitmq_service: Annotated[
        RabbitMQService,
        Depends(get_rabbitmq_service),
    ],
) -> AsyncGenerator[MovieService]:
    try:
        movie_service = MovieService(session, rabbitmq_service)
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
) -> AsyncGenerator[ReviewService]:
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
    redis_service: Annotated[
        CacheService,
        Depends(
            get_cache_service_for_confirmation_codes,
        ),
    ],
    http_request_service: Annotated[
        HttpRequestService,
        Depends(get_http_request_service),
    ],
) -> AsyncGenerator[UserService]:
    try:
        user_service = UserService(session, redis_service, http_request_service)
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
) -> AsyncGenerator[FavoriteMovieService]:
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
) -> AsyncGenerator[WatchHistoryService]:
    try:
        watch_history_service = WatchHistoryService(session)
        yield watch_history_service
    finally:
        """
        Действия после view.
        """
