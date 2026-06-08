import json
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import Any, cast

from aio_pika import IncomingMessage, Message
from aio_pika.abc import AbstractChannel

from packages.rabbitmq import RabbitMQService, connection


def get_message(
    message: IncomingMessage,
) -> dict[Any, Any]:
    decoded_body = message.body.decode()
    body_dictionary = json.loads(decoded_body)
    return body_dictionary  # type: ignore[no-any-return]


def create_message(body: dict[Any, Any]) -> Message:
    body_string = json.dumps(body)
    encoded_body = body_string.encode()
    message = Message(body=encoded_body)
    return message


@asynccontextmanager
async def get_channel() -> AsyncGenerator[AbstractChannel]:
    assert connection.RABBIT_MQ_CONNECTION is not None
    async with cast(
        AbstractChannel,
        connection.RABBIT_MQ_CONNECTION.channel(),
    ) as channel:
        yield channel


@asynccontextmanager
async def get_rabbitmq_service() -> AsyncGenerator[RabbitMQService]:
    async with get_channel() as channel:
        rabbitmq_service = RabbitMQService(channel)
        yield rabbitmq_service
