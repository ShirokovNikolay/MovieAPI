from typing import Any

from core.redis.client import RedisClient


class CacheService:
    def __init__(self, redis: RedisClient) -> None:
        self.redis = redis

    async def get(self, key: str, schema: Any = None) -> Any:
        value = await self.redis.get(key)
        if value is not None:
            return self.convert_string_to_object(value, schema)
        return None

    async def set(self, key: str, value: Any, ttl: int = 300) -> None:
        encoded_value = self.convert_object_to_string(value)
        await self.redis.set(key, encoded_value, ttl)

    async def expire(self, key: str, ttl: int) -> None:
        await self.redis.expire(key, ttl)

    async def exists(self, key: str) -> bool:
        return await self.redis.exists(key)

    async def delete(self, key: str) -> None:
        await self.redis.delete(key)

    async def delete_by_pattern(self, pattern: str) -> None:
        await self.redis.delete_by_pattern(pattern)

    @classmethod
    def create_cache_key(cls, prefix: str, **kwargs: Any) -> str:
        result = [prefix]
        for key, value in kwargs.items():
            result.append(f"{key}:{value}")
        return ":".join(result)

    @staticmethod
    def convert_string_to_object(value: str, schema: Any) -> Any:
        if schema is None:
            return value
        return schema.model_validate_json(value)

    @staticmethod
    def convert_object_to_string(value: Any) -> Any:
        if isinstance(
            value,
            (str, int, float, bool),
        ):
            return value
        return value.model_dump_json()
