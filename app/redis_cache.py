from typing import Any

from redis_client import RedisClient


class CacheService:
    def __init__(self, redis: RedisClient):
        self.redis = redis

    async def get(self, key: str, schema: Any) -> Any:
        if (value := await self.redis.get(key)) is not None:
            return self.string_to_object(value, schema)

    async def set(self, key: str, obj: Any, ttl: int = 300) -> None:
        value = self.object_to_string(obj)
        await self.redis.set(key, value, ttl)

    async def expire(self, key: str, ttl: int) -> None:
        await self.redis.expire(key, ttl)

    async def exists(self, key: str) -> bool:
        return await self.redis.exists(key)

    async def delete(self, key: str) -> None:
        await self.redis.delete(key)

    @staticmethod
    def string_to_object(value: str, schema: Any) -> Any:
        return schema.model_validate_json(value)

    @staticmethod
    def object_to_string(obj: Any) -> str:
        return obj.model_dump_json()
