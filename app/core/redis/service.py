from typing import Any, cast

from core.constants import AnyPydanticType, PrimitiveType
from core.redis.client import RedisClient


class RedisService:
    def __init__(self, redis: RedisClient) -> None:
        self.redis = redis

    async def get(
        self,
        key: str,
        schema: type[AnyPydanticType] | None = None,
        is_integer: bool = False,
        is_float: bool = False,
        is_boolean: bool = False,
    ) -> PrimitiveType | AnyPydanticType | None:
        if schema is not None:
            return await self._get_schema(key, schema)

        if is_integer:
            return await self._get_integer(key)

        if is_float:
            return await self._get_float(key)

        if is_boolean:
            return await self._get_boolean(key)

        return await self.redis.get(key)

    async def _get_schema(
        self,
        key: str,
        schema: type[AnyPydanticType],
    ) -> AnyPydanticType | None:
        value = await self.redis.get(key)
        if value is not None:
            return cast(AnyPydanticType, self.convert_string_to_object(value, schema))
        return None

    async def _get_integer(self, key: str) -> int | None:
        value = await self.redis.get(key)
        if value is not None:
            return int(value)
        return None

    async def _get_float(self, key: str) -> float | None:
        value = await self.redis.get(key)
        if value is not None:
            return float(value)
        return None

    async def _get_boolean(self, key: str) -> bool | None:
        boolean = {"True": True, "False": False}
        value = await self.redis.get(key)
        if value is not None:
            return boolean[value]
        return None

    async def set(self, key: str, value: Any, ttl: int = 300) -> None:
        encoded_value = self.convert_object_to_string(value)
        await self.redis.set(key, encoded_value, ttl)

    async def incr_by(self, key: str, amount: int = 1) -> int:
        return await self.redis.incr_by(key, amount)

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
    def convert_string_to_object(
        value: str | int, schema: type[AnyPydanticType],
    ) -> AnyPydanticType | PrimitiveType:
        if schema is None:
            return value
        return schema.model_validate_json(cast(str, value))

    @staticmethod
    def convert_object_to_string(value: Any) -> Any:
        if isinstance(
            value,
            (str, int, float, bool),
        ):
            return value
        return value.model_dump_json()
