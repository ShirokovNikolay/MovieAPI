from collections.abc import AsyncGenerator

from packages.rabbitmq.connection import init_rabbitmq
from packages.rabbitmq.utils import get_rabbitmq_service

# import aio_pika
# from packages.rabbitmq import connection
from core.rabbitmq.consumer import update_genre_url


async def start_rabbitmq() -> AsyncGenerator[None]:
    await init_rabbitmq()
    async with get_rabbitmq_service() as rabbitmq_service:
        queue_update = await rabbitmq_service.declare_queue(
            "update_genre_queue",
            durable=True,
        )

        exchange = await rabbitmq_service.declare_exchange(
            "to_monolith",
            "direct",
            durable=True,
        )
        await queue_update.bind(exchange, "to_monolith")
        await rabbitmq_service.consume(queue_update, update_genre_url)

        yield
