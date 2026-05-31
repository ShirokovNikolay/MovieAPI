from collections.abc import Callable

from aio_pika import Channel
from aio_pika.abc import (
    AbstractExchange,
    AbstractMessage,
    AbstractQueue,
)


class RabbitMQService:
    def __init__(self, channel: Channel) -> None:
        self.channel = channel

    async def declare_queue(
        self,
        name: str | None = None,
        durable: bool = False,
    ) -> AbstractQueue:
        return await self.channel.declare_queue(
            name=name,
            durable=durable,
        )

    async def declare_exchange(
        self,
        name: str,
        type: str = "direct",
        durable: bool = False,
    ) -> AbstractExchange:
        return await self.channel.declare_exchange(
            name=name,
            type=type,
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
