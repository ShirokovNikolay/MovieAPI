from collections.abc import Callable
from typing import TYPE_CHECKING

from aio_pika.abc import (
    AbstractChannel,
    AbstractExchange,
    AbstractMessage,
    AbstractQueue,
)

if TYPE_CHECKING:
    from packages.rabbitmq.constants import Exchange, ExchangeType, Queue


class RabbitMQService:
    def __init__(self, channel: AbstractChannel) -> None:
        self.channel = channel

    async def declare_queue(
        self,
        name: "Queue",
        durable: bool = True,
    ) -> AbstractQueue:
        return await self.channel.declare_queue(
            name=name.value,
            durable=durable,
        )

    async def declare_exchange(
        self,
        name: "Exchange",
        type: "ExchangeType",
        durable: bool = True,
    ) -> AbstractExchange:
        return await self.channel.declare_exchange(
            name=name.value,
            type=type.value,
            durable=durable,
        )

    async def bind(
        self,
        queue: AbstractQueue,
        exchange: AbstractExchange,
        routing_key: str | None = None,
    ) -> None:
        await queue.bind(
            exchange=exchange,
            routing_key=routing_key,
        )

    async def publish(
        self,
        message: AbstractMessage,
        routing_key: str,
        exchange: AbstractExchange,
    ) -> None:
        await exchange.publish(
            message=message,
            routing_key=routing_key,
        )

    async def consume(
        self,
        queue: AbstractQueue,
        callback: Callable,  # type: ignore # noqa: PGH003
    ) -> None:
        await queue.consume(callback=callback)
