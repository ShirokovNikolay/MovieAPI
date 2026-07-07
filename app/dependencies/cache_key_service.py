from collections.abc import AsyncGenerator
from typing import Annotated

from fastapi import Depends

from core.redis import RedisService
from core.redis.cache_key_service import CacheKeyService
from dependencies.redis_services import get_cache_versioning_redis_service


async def get_cache_key_service(
    cache_key_redis_service: Annotated[
        RedisService,
        Depends(
            get_cache_versioning_redis_service,
        ),
    ],
) -> AsyncGenerator[CacheKeyService]:
    try:
        cache_key_service = CacheKeyService(cache_key_redis_service)
        yield cache_key_service
    finally:
        """
        Действия после view.
        """
