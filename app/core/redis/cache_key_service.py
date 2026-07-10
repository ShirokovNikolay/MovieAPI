from typing import cast

from core.config import settings
from core.constants import CacheEntity, PrimitiveType
from core.redis import RedisService


class CacheKeyService:
    list_field = "list"

    def __init__(self, redis: RedisService) -> None:
        self.redis = redis

    async def __init_version(self, entity: CacheEntity) -> int:
        key = self.__create_version_entity_key(entity)
        start_value = 1
        await self.redis.set(
            key=key,
            value=start_value,
        )
        return start_value

    async def __get_version(self, entity: CacheEntity) -> int:
        key = self.__create_version_entity_key(entity)
        version = await self.redis.get(key, is_integer=True)
        return cast(int, version)

    async def __update_version(self, entity: CacheEntity) -> None:
        key = self.__create_version_entity_key(entity)
        await self.redis.incr_by(key, amount=1)

    @classmethod
    def __create_version_entity_key(cls, entity: CacheEntity) -> str:
        return f"{settings.service_name}:version:{cls.list_field}:{entity.value}"

    async def invalidate_list_keys(
        self,
        entity: CacheEntity,
    ) -> None:
        await self.__update_version(
            entity=entity,
        )

    @staticmethod
    def build_item_key(
        entity: CacheEntity,
        entity_id: int | tuple,
        action: str = "get",
        **params: PrimitiveType,
    ) -> str:
        key = f"{settings.service_name}:{entity.value}:{entity_id}:{action}"
        for parameter_name, value in params.items():
            key = f"{key}:{parameter_name}:{value}"

        return key

    @classmethod
    def build_item_regex_key(
        cls,
        entity: CacheEntity,
        entity_id_regex: int | str,
        action_regex: str = "get",
        **params: PrimitiveType,
    ) -> str:
        return cls.build_item_key(
            entity=entity,
            entity_id=entity_id_regex,
            action=action_regex,
            **params,
        )

    async def build_list_key(
        self,
        entity: CacheEntity,
        action: str = "get",
        **params: PrimitiveType,
    ) -> str:
        version = await self.__get_version(entity)
        if version is None:
            version = await self.__init_version(entity)
        key = f"{settings.service_name}:{entity.value}:{self.list_field}:version:{version}:{action}"  # noqa: E501

        for parameter_name, value in params.items():
            key = f"{key}:{parameter_name}:{value}"

        return key

    async def build_list_regex_key(
        self,
        entity: CacheEntity,
        action_regex: str = "get",
        **params: PrimitiveType,
    ) -> str:
        return await self.build_list_key(
            entity=entity,
            action=action_regex,
            **params,
        )
