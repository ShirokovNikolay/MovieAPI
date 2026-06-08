from collections.abc import AsyncGenerator
from typing import Annotated

from aio_pika.abc import AbstractChannel
from fastapi import Depends

from packages.rabbitmq.connection import get_channel
from packages.rabbitmq.service import RabbitMQService


async def get_rabbit_mq_service(
    channel: Annotated[
        AbstractChannel,
        Depends(get_channel),
    ],
) -> AsyncGenerator[RabbitMQService]:
    try:
        yield RabbitMQService(channel)
    finally:
        """
        Действия после бизнес логики.
        """
