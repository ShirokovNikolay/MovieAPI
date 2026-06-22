from collections.abc import AsyncGenerator, Callable
from typing import Annotated

from fastapi import Depends

from core.redis import RedisClient, RedisService
from dependencies.redis_client import (
    get_auth_redis_client,
    get_favorite_movie_redis_client,
    get_genre_redis_client,
    get_movie_redis_client,
    get_review_redis_client,
    get_user_redis_client,
    get_watch_history_redis_client,
)


def redis_service_factory(
    redis_dependency: Callable[[], AsyncGenerator[RedisClient]],
) -> Callable[
    [RedisClient],
    AsyncGenerator[RedisService],
]:
    async def dependency(
        redis: Annotated[
            RedisClient,
            Depends(redis_dependency),
        ],
    ) -> AsyncGenerator[RedisService]:
        try:
            redis_service = RedisService(redis)
            yield redis_service
        finally:
            """
            Действия после view.
            """

    return dependency


get_genre_redis_service = redis_service_factory(
    get_genre_redis_client,
)
get_movie_redis_service = redis_service_factory(
    get_movie_redis_client,
)
get_review_redis_service = redis_service_factory(
    get_review_redis_client,
)
get_favorite_movie_redis_service = redis_service_factory(
    get_favorite_movie_redis_client,
)
get_watch_history_redis_service = redis_service_factory(
    get_watch_history_redis_client,
)
get_user_redis_service = redis_service_factory(
    get_user_redis_client,
)
get_auth_redis_service = redis_service_factory(
    get_auth_redis_client,
)
