# from contextlib import asynccontextmanager
# from time import sleep
# from typing import AsyncIterator
#
# from fastapi import FastAPI
#
# from packages.rabbit_mq import get_rabbit_mq_service
# from packages.rabbit_mq.connection import RABBIT_MQ_CONNECTION, init_rabbit_mq
#
#
# @asynccontextmanager
# async def lifespan(app: FastAPI) -> AsyncIterator[None]:
#     await init_rabbit_mq()
#     channel = await RABBIT_MQ_CONNECTION.channel()
#     async for rabbitmq in get_rabbit_mq_service(channel):
#         queue_copy = await rabbitmq.declare_queue("copy_file_queue", durable=True)
#         queue_delete = await rabbitmq.declare_queue("delete_tmp_queue", durable=True)
#
#         exchange = await rabbitmq.declare_exchange("to_mediaservice", "direct")
#
#         await queue_copy.bind(exchange, "to_mediaservice")
#         await queue_delete.bind(exchange, "to_mediaservice")
#     yield
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

import aio_pika
from fastapi import FastAPI
from packages.rabbit_mq import connection, get_rabbit_mq_service

from rabbitmq_consumer import copy_file, delete_temporary_file


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:  # noqa: ARG001
    connection.RABBIT_MQ_CONNECTION = await aio_pika.connect_robust(
        url="amqp://guest:guest@rabbitmq:5672",
    )

    channel = await connection.RABBIT_MQ_CONNECTION.channel()

    async for rabbitmq in get_rabbit_mq_service(channel):
        queue_copy = await rabbitmq.declare_queue(
            "copy_file_queue",
            durable=True,
        )
        queue_delete = await rabbitmq.declare_queue(
            "delete_tmp_queue",
            durable=True,
        )

        exchange = await rabbitmq.declare_exchange(
            "to_mediaservice",
            "direct",
            durable=True,
        )

        await queue_copy.bind(exchange, "to_mediaservice")
        await queue_delete.bind(exchange, "to_mediaservice")

        await rabbitmq.consume(queue_copy, copy_file)
        await rabbitmq.consume(queue_delete, delete_temporary_file)
    yield
    await connection.RABBIT_MQ_CONNECTION.close()
