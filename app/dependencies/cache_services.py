from typing import Annotated

from fastapi import Depends

from cache_services import GenreCacheService
from dependencies.redis_client import get_redis_client_for_genres
from dependencies.services import get_genre_service
from redis_cache import CacheService
from redis_client import RedisClient
from services import GenreService


async def get_cache_service_for_genres(
    redis: Annotated[
        RedisClient,
        Depends(get_redis_client_for_genres),
    ],
):
    try:
        genre_cache_service = CacheService(redis)
        yield genre_cache_service
    finally:
        """
        Действия после view.
        """


async def get_genre_cache_service(
    genre_service: Annotated[
        GenreService,
        Depends(get_genre_service),
    ],
    cache_service: Annotated[
        CacheService,
        Depends(get_cache_service_for_genres),
    ],
):
    try:
        genre_cache_service = GenreCacheService(genre_service, cache_service)
        yield genre_cache_service
    finally:
        """
        Действия после view.
        """
