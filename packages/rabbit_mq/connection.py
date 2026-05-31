from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

import aio_pika
from aio_pika.abc import AbstractChannel

from core.config import settings

RABBIT_MQ_CONNECTION = None


async def init_rabbit_mq() -> None:
    global RABBIT_MQ_CONNECTION  # noqa: PLW0603
    RABBIT_MQ_CONNECTION = await aio_pika.connect_robust(
        url=settings.rabbitmq.url_rabbitmq,
    )


async def close_rabbit_mq() -> None:
    global RABBIT_MQ_CONNECTION  # noqa: PLW0602
    if RABBIT_MQ_CONNECTION is not None:
        await RABBIT_MQ_CONNECTION.close()


@asynccontextmanager
async def get_channel() -> AsyncGenerator[AbstractChannel]:
    if RABBIT_MQ_CONNECTION is None:
        raise aio_pika.exceptions.ConnectionClosed
    try:
        channel = await RABBIT_MQ_CONNECTION.channel()
        yield channel
    finally:
        await channel.close()
