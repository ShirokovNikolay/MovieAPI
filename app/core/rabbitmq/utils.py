from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import cast

from aio_pika.abc import AbstractChannel
from packages.rabbit_mq import RabbitMQService, connection
from sqlalchemy.ext.asyncio import AsyncSession

from cache_services import GenreCacheService
from core.database import session_factory
from core.redis import CacheService, RedisClient
from dependencies.redis_client import get_redis_client_for_genres
from services import GenreService


@asynccontextmanager
async def get_session() -> AsyncGenerator[AsyncSession]:
    async with session_factory() as session:
        yield session


@asynccontextmanager
async def get_channel() -> AsyncGenerator[AbstractChannel]:
    assert connection.RABBIT_MQ_CONNECTION is not None
    async with cast(
        AbstractChannel,
        connection.RABBIT_MQ_CONNECTION.channel(),
    ) as channel:
        yield channel


@asynccontextmanager
async def get_rabbitmq_service() -> AsyncGenerator[RabbitMQService]:
    async with get_channel() as channel:
        rabbitmq_service = RabbitMQService(channel)
        yield rabbitmq_service


@asynccontextmanager
async def get_genre_service() -> AsyncGenerator[GenreService]:
    async with get_session() as session, get_rabbitmq_service() as rabbitmq_service:
        genre_service = GenreService(session, rabbitmq_service)
        yield genre_service


@asynccontextmanager
async def get_get_redis_client_for_genres() -> AsyncGenerator[RedisClient]:
    async for redis_client in get_redis_client_for_genres():
        yield redis_client


@asynccontextmanager
async def get_cache_service_for_genres() -> AsyncGenerator[CacheService]:
    async with get_get_redis_client_for_genres() as redis_client:
        cache_service = CacheService(redis_client)
        yield cache_service


@asynccontextmanager
async def get_genre_cache_service() -> AsyncGenerator[GenreCacheService]:
    async with (
        get_genre_service() as genre_service,
        get_cache_service_for_genres() as cache_service,
    ):
        genre_cache_service = GenreCacheService(genre_service, cache_service)
        yield genre_cache_service
