from collections.abc import AsyncGenerator

from packages.rabbitmq.connection import rabbitmq_connection_startup
from packages.rabbitmq.constants import Exchange, ExchangeType, Queue
from packages.rabbitmq.utils import get_rabbitmq_service

from core.rabbitmq.consumers import (
    update_genre_poster_url,
    update_movie_poster_url,
    update_movie_source_url,
    update_watch_history_cache_on_watch_movie,
)


async def rabbitmq_consumer_queues_startup() -> AsyncGenerator[None]:
    async with get_rabbitmq_service() as rabbitmq_service:
        exchange = await rabbitmq_service.declare_exchange(
            name=Exchange.media_service,
            type=ExchangeType.direct,
            durable=True,
        )
        queue_update_genre_poster_url = await rabbitmq_service.declare_queue(
            name=Queue.update_genre_poster_url,
            durable=True,
        )
        queue_update_movie_poster_url = await rabbitmq_service.declare_queue(
            name=Queue.update_movie_poster_url,
            durable=True,
        )
        queue_update_movie_source_url = await rabbitmq_service.declare_queue(
            name=Queue.update_movie_source_url,
            durable=True,
        )

        ###
        app_exchange = await rabbitmq_service.declare_exchange(
            name=Exchange.app,
            type=ExchangeType.direct,
            durable=True,
        )
        queue_update_watch_history_cache_on_watch_movie = (
            await rabbitmq_service.declare_queue(
                name=Queue.update_watch_history_cache_on_watch_movie,
                durable=True,
            )
        )
        await rabbitmq_service.bind(
            queue_update_watch_history_cache_on_watch_movie,
            app_exchange,
            Queue.update_watch_history_cache_on_watch_movie.value,
        )
        await rabbitmq_service.consume(
            queue_update_watch_history_cache_on_watch_movie,
            update_watch_history_cache_on_watch_movie,
        )
        ####

        await rabbitmq_service.bind(
            queue_update_genre_poster_url,
            exchange,
            Queue.update_genre_poster_url.value,
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
        await rabbitmq_service.consume(
            queue_update_genre_poster_url,
            update_genre_poster_url,
        )
        await rabbitmq_service.consume(
            queue_update_movie_poster_url,
            update_movie_poster_url,
        )
        await rabbitmq_service.consume(
            queue_update_movie_source_url,
            update_movie_source_url,
        )
        yield


async def rabbitmq_startup() -> AsyncGenerator[None]:
    await rabbitmq_connection_startup()
    rabbitmq = rabbitmq_consumer_queues_startup()
    await anext(rabbitmq)
    yield
