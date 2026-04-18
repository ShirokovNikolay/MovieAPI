from typing import Self

from redis.asyncio import Redis
from core.config import settings


class RedisClient:
    def __init__(
        self,
        host: str = settings.redis.connection.host,
        port: int = settings.redis.connection.port,
        db: int = settings.redis.db.rate_limiter,
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

    async def delete_by_pattern(self, pattern: str) -> None:
        async for key in self._redis.scan_iter(match=pattern):
            await self.delete(key)

    async def expire(self, key: str, ttl: int = 300) -> None:
        await self._redis.expire(key, ttl)

    async def get_ttl(self, key: str) -> int | None:
        return await self._redis.ttl(key)

    async def incr_by(self, key: str, amount: int = 1) -> int:
        return await self._redis.incrby(key, amount)

    async def zget_all_members(self, key: str) -> list[str]:
        return await self._redis.zrange(key, 0, -1, withscores=False)

    async def zget_all_members_with_scores(self, key: str) -> list[tuple]:
        return await self._redis.zrange(key, 0, -1, withscores=True)

    async def zadd(self, key: str, pairs: dict[str, str]) -> None:
        """
        Параметр pairs - словарь, в котором содержатся пары ключ - значение вида member - score.
        """
        await self._redis.zadd(key, pairs)

    async def zcard(self, key: str) -> int:
        """
        Возвращает количество member в отсортированном множестве по ключу key.
        """
        return await self._redis.zcard(key)

    async def zrem(self, key: str, *values: str) -> None:
        await self._redis.zrem(key, *values)

    async def zremrangebyscore(
        self, key: str, min_value: float, max_value: float
    ) -> int:
        return await self._redis.zremrangebyscore(key, min_value, max_value)
