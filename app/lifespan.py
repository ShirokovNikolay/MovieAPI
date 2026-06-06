from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

import aio_pika
from fastapi import FastAPI
from packages.rabbit_mq import connection, get_rabbit_mq_service

from core.rabbitmq_consumer import update_genre_url


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:  # noqa: ARG001
    """
    Действия до старта приложения.
    """
    # await init_rabbit_mq()
    # await init_admin()
    # global RABBIT_MQ_CONNECTION  # Обязательно! Чтобы переменная не была None
    connection.RABBIT_MQ_CONNECTION = await aio_pika.connect_robust(
        url="amqp://guest:guest@rabbitmq:5672",
    )
    # for _ in range(10):  # Ждем, пока RabbitMQ окончательно поднимет порт
    #     try:
    #         connection.RABBIT_MQ_CONNECTION = await aio_pika.connect_robust(
    #             url="amqp://guest:guest@rabbitmq:5672/%2f"
    #         )
    #         break
    #     except (AMQPConnectionError, OSError):
    #         await asyncio.sleep(2)
    #
    # if not connection.RABBIT_MQ_CONNECTION:
    #     raise RuntimeError("RabbitMQ недоступен")

    channel = await connection.RABBIT_MQ_CONNECTION.channel()
    async for rabbitmq in get_rabbit_mq_service(channel):
        queue_update = await rabbitmq.declare_queue(
            "update_genre_queue",
            durable=True,
        )

        exchange = await rabbitmq.declare_exchange(
            "to_monolith",
            "direct",
            durable=True,
        )

        await queue_update.bind(exchange, "to_monolith")
        await rabbitmq.consume(queue_update, update_genre_url)
    yield
    """
    Действия после заверения работы приложения.
    """
    # await close_rabbit_mq()
