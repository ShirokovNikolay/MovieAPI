from collections.abc import AsyncGenerator

from packages.constants import Exchange, ExchangeType, Queue
from packages.rabbitmq.connection import init_rabbitmq
from packages.rabbitmq.utils import get_rabbitmq_service

from core.rabbitmq.consumer import update_genre_url


async def start_rabbitmq() -> AsyncGenerator[None]:
    await init_rabbitmq()
    async with get_rabbitmq_service() as rabbitmq_service:
        queue_update = await rabbitmq_service.declare_queue(
            name=Queue.update_genre_url.value,
            durable=True,
        )

        exchange = await rabbitmq_service.declare_exchange(
            name=Exchange.mediaservice.value,
            type=ExchangeType.direct.value,
            durable=True,
        )
        await queue_update.bind(exchange, Queue.update_genre_url.value)
        await rabbitmq_service.consume(queue_update, update_genre_url)

        yield
