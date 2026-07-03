from core.config import settings
from core.constants import PrimitiveType
from core.redis import RedisService


class CacheKeyService:
    list_field = "list"

    def __init__(self, redis: RedisService) -> None:
        self.redis = redis

    async def __build(
        self,
        entity: str,
        action: str,
        entity_id: int | None = None,
        **params: PrimitiveType,
    ) -> str:
        if entity_id is None:
            version = await self.__get_version(entity)
            if version is None:
                await self.__init_version(entity)
            key = f"{settings.service_name}:{entity}:{self.list_field}:version:{version}:{action}"
        else:
            key = f"{settings.service_name}:{entity}:{entity_id}:{action}"

        for parameter_name, value in params.items():
            key = f"{key}:{parameter_name}:{value}"

        return key

    async def __get_version(self, entity: str) -> int:
        key = self.__create_version_entity_key(entity)
        version = await self.redis.get(key, is_integer=True)
        if not await self.redis.exists(key):
            raise ValueError
        return version

    async def __update_version(self, entity: str) -> None:
        key = self.__create_version_entity_key(entity)
        await self.redis.incr_by(key, amount=1)

    async def __init_version(self, entity: str) -> None:
        key = self.__create_version_entity_key(entity)
        await self.redis.set(
            key=key,
            value=1,
        )

    @classmethod
    def __create_version_entity_key(cls, entity: str) -> str:
        return f"{settings.service_name}:{cls.list_field}:{entity}:version"

    async def invalidate_list_keys(
        self,
        entity: str,
    ) -> None:
        await self.__update_version(
            entity=entity,
        )

    async def build_item_key(
        self,
        entity: str,
        action: str,
        entity_id: int,
        **params: PrimitiveType,
    ) -> str:
        return await self.__build(
            entity=entity,
            entity_id=entity_id,
            action=action,
            **params,
        )

    async def build_list_key(
        self,
        entity: str,
        action: str,
        **params: PrimitiveType,
    ) -> str:
        return await self.__build(
            entity=entity,
            action=action,
            **params,
        )
