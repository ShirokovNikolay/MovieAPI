from collections.abc import AsyncGenerator

import aio_pika
from aio_pika.abc import AbstractChannel

RABBIT_MQ_CONNECTION = None


async def init_rabbit_mq() -> None:
    global RABBIT_MQ_CONNECTION  # noqa: PLW0603
    RABBIT_MQ_CONNECTION = await aio_pika.connect_robust(
        url="amqp://guest:guest@rabbitmq:5672/%2f",
    )


async def close_rabbit_mq() -> None:
    global RABBIT_MQ_CONNECTION  # noqa: PLW0602
    if RABBIT_MQ_CONNECTION is not None:
        await RABBIT_MQ_CONNECTION.close()


async def get_channel() -> AsyncGenerator[AbstractChannel]:
    if RABBIT_MQ_CONNECTION is None:
        raise aio_pika.exceptions.ConnectionClosed
    try:
        channel = await RABBIT_MQ_CONNECTION.channel()
        yield channel
    finally:
        await channel.close()
