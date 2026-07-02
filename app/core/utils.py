from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from packages.rabbitmq.utils import get_rabbitmq_service
from sqlalchemy.ext.asyncio import AsyncSession

from cache_services import GenreCacheService, MovieCacheService
from core.database import session_factory
from core.redis import RedisClient, RedisService
from dependencies.redis_client import (
    get_genre_redis_client as get_genre_redis_client_dependency,
)
from dependencies.redis_client import (
    get_movie_redis_client as get_movie_redis_client_dependency,
)
from dependencies.redis_client import (
    get_watch_history_redis_client as get_watch_history_redis_client_dependency,
)
from services import GenreService, MovieService, UserService


@asynccontextmanager
async def get_session() -> AsyncGenerator[AsyncSession]:
    async with session_factory() as session:
        yield session


@asynccontextmanager
async def get_user_service() -> AsyncGenerator[UserService]:
    async with get_session() as session:
        user_service = UserService(session)
        yield user_service


@asynccontextmanager
async def get_genre_service() -> AsyncGenerator[GenreService]:
    async with get_session() as session, get_rabbitmq_service() as rabbitmq_service:
        genre_service = GenreService(session, rabbitmq_service)
        yield genre_service


@asynccontextmanager
async def get_genre_redis_client() -> AsyncGenerator[RedisClient]:
    async for redis_client in get_genre_redis_client_dependency():
        yield redis_client


@asynccontextmanager
async def get_genre_redis_service() -> AsyncGenerator[RedisService]:
    async with get_genre_redis_client() as redis_client:
        redis_service = RedisService(redis_client)
        yield redis_service


@asynccontextmanager
async def get_genre_cache_service() -> AsyncGenerator[GenreCacheService]:
    async with (
        get_genre_service() as genre_service,
        get_genre_redis_service() as cache_service,
    ):
        genre_cache_service = GenreCacheService(genre_service, cache_service)
        yield genre_cache_service


@asynccontextmanager
async def get_movie_service() -> AsyncGenerator[MovieService]:
    async with get_session() as session, get_rabbitmq_service() as rabbitmq_service:
        movie_service = MovieService(session, rabbitmq_service)
        yield movie_service


@asynccontextmanager
async def get_movie_redis_client() -> AsyncGenerator[RedisClient]:
    async for redis_client in get_movie_redis_client_dependency():
        yield redis_client


@asynccontextmanager
async def get_movie_redis_service() -> AsyncGenerator[RedisService]:
    async with get_movie_redis_client() as redis_client:
        cache_service = RedisService(redis_client)
        yield cache_service


@asynccontextmanager
async def get_watch_history_redis_client() -> AsyncGenerator[RedisClient]:
    async for redis_client in get_watch_history_redis_client_dependency():
        yield redis_client


@asynccontextmanager
async def get_watch_history_redis_service() -> AsyncGenerator[RedisService]:
    async with get_watch_history_redis_client() as redis_client:
        cache_service = RedisService(redis_client)
        yield cache_service


@asynccontextmanager
async def get_movie_cache_service() -> AsyncGenerator[MovieCacheService]:
    async with (
        get_movie_service() as movie_service,
        get_movie_redis_service() as cache_service_for_movies,
        get_watch_history_redis_service() as cache_service_for_watch_history,
    ):
        movie_cache_service = MovieCacheService(
            movie_service,
            cache_service_for_movies,
            cache_service_for_watch_history,
        )
        yield movie_cache_service
