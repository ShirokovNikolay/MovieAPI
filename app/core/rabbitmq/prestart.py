from collections.abc import AsyncGenerator

from packages.constants import Exchange, ExchangeType, Queue
from packages.rabbitmq.connection import init_rabbitmq
from packages.rabbitmq.utils import get_rabbitmq_service

from core.rabbitmq.consumer import (
    update_genre_poster_url,
    update_movie_poster_url,
    update_movie_source_url,
)


async def start_rabbitmq() -> AsyncGenerator[None]:
    await init_rabbitmq()
    async with get_rabbitmq_service() as rabbitmq_service:
        queue_update_genre_url = await rabbitmq_service.declare_queue(
            name=Queue.update_genre_url.value,
            durable=True,
        )
        queue_update_movie_poster_url = await rabbitmq_service.declare_queue(
            name=Queue.update_movie_poster_url.value,
            durable=True,
        )
        queue_update_movie_source_url = await rabbitmq_service.declare_queue(
            name=Queue.update_movie_source_url.value,
            durable=True,
        )

        exchange = await rabbitmq_service.declare_exchange(
            name=Exchange.mediaservice.value,
            type=ExchangeType.direct.value,
            durable=True,
        )
        await rabbitmq_service.bind(
            queue_update_genre_url,
            exchange,
            Queue.update_genre_url.value,
        )
        await rabbitmq_service.bind(
            queue_update_movie_poster_url,
            exchange,
            Queue.update_movie_poster_url.value,
        )
        await rabbitmq_service.bind(
            queue_update_movie_source_url,
            exchange,
            Queue.update_movie_source_url.value,
        )
        await rabbitmq_service.consume(queue_update_genre_url, update_genre_poster_url)
        await rabbitmq_service.consume(
            queue_update_movie_poster_url,
            update_movie_poster_url,
        )
        await rabbitmq_service.consume(
            queue_update_movie_source_url,
            update_movie_source_url,
        )

        yield
