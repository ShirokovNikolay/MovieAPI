from collections.abc import AsyncGenerator

from packages.constants import Exchange, ExchangeType, Queue
from packages.rabbitmq.connection import rabbitmq_connection_startup
from packages.rabbitmq.utils import get_rabbitmq_service

from core.rabbitmq.consumer import copy_file, delete_file


async def rabbitmq_consumer_queues_startup() -> AsyncGenerator[None]:
    async with get_rabbitmq_service() as rabbitmq_service:
        exchange = await rabbitmq_service.declare_exchange(
            name=Exchange.app.value,
            type=ExchangeType.direct.value,
            durable=True,
        )
        queue_copy = await rabbitmq_service.declare_queue(
            name=Queue.copy_file.value,
            durable=True,
        )
        queue_delete = await rabbitmq_service.declare_queue(
            name=Queue.delete_file.value,
            durable=True,
        )

        await rabbitmq_service.bind(queue_copy, exchange, Queue.copy_file.value)
        await rabbitmq_service.bind(queue_delete, exchange, Queue.delete_file.value)

        await rabbitmq_service.consume(queue_copy, copy_file)
        await rabbitmq_service.consume(queue_delete, delete_file)
        yield


async def rabbitmq_startup() -> AsyncGenerator[None]:
    await rabbitmq_connection_startup()
    rabbitmq = rabbitmq_consumer_queues_startup()
    await anext(rabbitmq)
    yield
