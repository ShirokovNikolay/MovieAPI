from typing import Annotated

from fastapi import Depends

from core.redis import RedisClient, CacheService
from dependencies.redis_client import (
    get_redis_client_for_genres,
    get_redis_client_for_movies,
    get_redis_client_for_favorite_movies,
    get_redis_client_for_watch_history,
    get_redis_client_for_reviews,
    get_redis_client_for_users,
)


def cache_service_factory(redis_dependency):
    async def dependency(
        redis: Annotated[
            RedisClient,
            Depends(redis_dependency),
        ],
    ):
        try:
            cache_service = CacheService(redis)
            yield cache_service
        finally:
            """
            Действия после view.
            """

    return dependency


get_cache_service_for_genres = cache_service_factory(
    get_redis_client_for_genres,
)
get_cache_service_for_movies = cache_service_factory(
    get_redis_client_for_movies,
)
get_cache_service_for_reviews = cache_service_factory(
    get_redis_client_for_reviews,
)
get_cache_service_for_favorite_movies = cache_service_factory(
    get_redis_client_for_favorite_movies
)
get_cache_service_for_watch_history = cache_service_factory(
    get_redis_client_for_watch_history
)
get_cache_service_for_users = cache_service_factory(
    get_redis_client_for_users,
)
