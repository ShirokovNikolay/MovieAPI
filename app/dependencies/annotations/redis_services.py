from typing import Annotated

from fastapi import Depends

from core.redis import RedisService
from dependencies.redis_services import (
    get_favorite_movie_redis_service,
    get_genre_redis_service,
    get_movie_redis_service,
    get_review_redis_service,
    get_user_redis_service,
    get_watch_history_redis_service,
)

GenreRedisServiceDep = Annotated[
    RedisService,
    Depends(get_genre_redis_service),
]

MovieRedisServiceDep = Annotated[
    RedisService,
    Depends(get_movie_redis_service),
]

FavoriteMovieRedisServiceDep = Annotated[
    RedisService,
    Depends(
        get_favorite_movie_redis_service,
    ),
]

ReviewRedisServiceDep = Annotated[
    RedisService,
    Depends(
        get_review_redis_service,
    ),
]

UserRedisServiceDep = Annotated[
    RedisService,
    Depends(
        get_user_redis_service,
    ),
]

WatchHistoryRedisServiceDep = Annotated[
    RedisService,
    Depends(
        get_watch_history_redis_service,
    ),
]
