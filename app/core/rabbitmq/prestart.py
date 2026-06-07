from collections.abc import AsyncGenerator

import aio_pika
from packages.rabbit_mq import connection

from core.rabbitmq.consumer import update_genre_url
from core.rabbitmq.utils import get_rabbitmq_service


async def start_rabbitmq() -> AsyncGenerator[None]:
    assert connection.RABBIT_MQ_CONNECTION is not None
    connection.RABBIT_MQ_CONNECTION = await aio_pika.connect_robust(
        url="amqp://guest:guest@rabbitmq:5672",
    )
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
