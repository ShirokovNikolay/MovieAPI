import json
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from aio_pika import IncomingMessage, Message
from packages.rabbit_mq import RabbitMQService, connection

from cache_services import GenreCacheService
from core.config import settings
from core.constants import BASE_MINIO_URL
from core.database import session_factory
from core.redis import CacheService
from dependencies.redis_client import redis_client_factory
from schemas.genre import GenrePartialUpdate
from services import GenreService


@asynccontextmanager
async def get_genre_cache_service() -> AsyncGenerator[GenreCacheService]:
    async with (
        session_factory() as session,
        connection.RABBIT_MQ_CONNECTION.channel() as channel,  # type: ignore[union-attr]
    ):
        rabbit_mq_service = RabbitMQService(channel)
        genre_service = GenreService(session, rabbit_mq_service)
        get_redis_client_for_genres = redis_client_factory(
            db=settings.redis.db.genres,
        )
        async for redis_client in get_redis_client_for_genres():
            cache_service = CacheService(redis_client)
            genre_cache_service = GenreCacheService(
                genre_service=genre_service,
                cache_service=cache_service,
            )
            yield genre_cache_service


async def update_genre_url(message: IncomingMessage) -> None:
    async with message.process(), get_genre_cache_service() as genre_cache_service:
        data = json.loads(message.body.decode())
        genre_id, bucket_name, object_name, new_object_name = (
            data["genre_id"],
            data["bucket_name"],
            data["object_name"],
            data["new_object_name"],
        )
        genre_partial_update = GenrePartialUpdate(
            preview_url=BASE_MINIO_URL + "/genre-posters/" + new_object_name,
        )
        await genre_cache_service.partial_update_genre(
            genre_id=genre_id,
            update_data=genre_partial_update,
        )

        rabbitmq_service = genre_cache_service.genre_service.rabbitmq_service
        exchange = await rabbitmq_service.declare_exchange(
            name="to_mediaservice",
            type="direct",
        )
        body = {
            "object_name": object_name,
            "bucket_name": bucket_name,
        }
        await rabbitmq_service.publish(
            message=Message(
                body=json.dumps(body).encode(),
            ),
            exchange=exchange,
            routing_key="to_mediaservice",
        )
