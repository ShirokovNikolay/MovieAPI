from collections.abc import AsyncGenerator
from typing import Annotated

from aio_pika import Channel
from fastapi import Depends

from packages.rabbit_mq import RabbitMQService
from packages.rabbit_mq.connection import get_channel


async def get_rabbit_mq_service(
    channel: Annotated[
        Channel,
        Depends(get_channel),
    ],
) -> AsyncGenerator[RabbitMQService]:
    try:
        yield RabbitMQService(channel)
    finally:
        """
        Действия после бизнес логики.
        """
