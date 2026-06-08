from collections.abc import AsyncGenerator

from packages.rabbitmq.connection import init_rabbitmq
from packages.rabbitmq.utils import get_rabbitmq_service

from rabbitmq.consumer import copy_file, delete_temporary_file


async def start_rabbitmq() -> AsyncGenerator[None]:
    await init_rabbitmq()
    async with get_rabbitmq_service() as rabbitmq_service:
        queue_copy = await rabbitmq_service.declare_queue(
            "copy_file_queue",
            durable=True,
        )
        queue_delete = await rabbitmq_service.declare_queue(
            "delete_tmp_queue",
            durable=True,
        )

        exchange = await rabbitmq_service.declare_exchange(
            "to_mediaservice",
            "direct",
            durable=True,
        )

        await queue_copy.bind(exchange, "to_mediaservice")
        await queue_delete.bind(exchange, "to_mediaservice")

        await rabbitmq_service.consume(queue_copy, copy_file)
        await rabbitmq_service.consume(queue_delete, delete_temporary_file)
        yield
