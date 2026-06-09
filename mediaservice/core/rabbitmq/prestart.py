from collections.abc import AsyncGenerator

from packages.constants import Exchange, ExchangeType, Queue
from packages.rabbitmq.connection import init_rabbitmq
from packages.rabbitmq.utils import get_rabbitmq_service

from core.rabbitmq.consumer import copy_file, delete_file


async def start_rabbitmq() -> AsyncGenerator[None]:
    await init_rabbitmq()
    async with get_rabbitmq_service() as rabbitmq_service:
        queue_copy = await rabbitmq_service.declare_queue(
            name=Queue.copy_file.value,
            durable=True,
        )
        queue_delete = await rabbitmq_service.declare_queue(
            name=Queue.delete_file.value,
            durable=True,
        )

        exchange = await rabbitmq_service.declare_exchange(
            name=Exchange.app.value,
            type=ExchangeType.direct.value,
            durable=True,
        )

        await rabbitmq_service.bind(queue_copy, exchange, Queue.copy_file.value)
        await rabbitmq_service.bind(queue_delete, exchange, Queue.delete_file.value)

        await rabbitmq_service.consume(queue_copy, copy_file)
        await rabbitmq_service.consume(queue_delete, delete_file)
        yield
