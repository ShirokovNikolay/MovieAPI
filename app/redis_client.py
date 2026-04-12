from typing import Self

from redis.asyncio import Redis
from core.config import settings


class RedisClient:
    def __init__(
        self,
        host: str = settings.redis.connection.host,
        port: int = settings.redis.connection.port,
        db: int = settings.redis.db.default,
        decode_responses: bool = True,
    ):
        self._redis = Redis(
            host=host,
            port=port,
            db=db,
            decode_responses=decode_responses,
        )

    async def __aenter__(self) -> Self:
        """
        Действия при инициализации redis через асинхронный контекстный менеджер.
        """
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        """
        Действия после выхода из асинхронного контекстного менеджера.
        """
        await self._redis.close()

    async def get(self, key: str) -> str | None:
        return await self._redis.get(key)

    async def exists(self, key: str) -> bool:
        return await self._redis.exists(key)

    async def set(self, key: str, value: str, expire: int) -> None:
        await self._redis.set(
            key,
            value,
            ex=expire,
        )

    async def delete(self, key: str) -> None:
        await self._redis.delete(key)

    async def expire(self, key: str, ttl: int = 300) -> None:
        await self._redis.expire(key, ttl)

    async def get_ttl(self, key: str) -> int | None:
        return await self._redis.ttl(key)

    async def incr_by(self, key: str, amount: int = 1) -> int:
        return await self._redis.incrby(key, amount)
