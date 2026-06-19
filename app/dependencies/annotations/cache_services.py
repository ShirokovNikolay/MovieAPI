from typing import Annotated

from fastapi import Depends

from cache_services import (
    FavoriteMovieCacheService,
    GenreCacheService,
    MovieCacheService,
    ReviewCacheService,
    UserCacheService,
    WatchHistoryCacheService,
)
from core.redis import RedisService
from dependencies.cache_services import (
    get_favorite_movie_cache_service,
    get_genre_cache_service,
    get_movie_cache_service,
    get_review_cache_service,
    get_user_cache_service,
    get_watch_history_cache_service,
)
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

GenreCacheServiceDep = Annotated[
    GenreCacheService,
    Depends(
        get_genre_cache_service,
    ),
]

MovieCacheServiceDep = Annotated[
    MovieCacheService,
    Depends(
        get_movie_cache_service,
    ),
]

FavoriteMovieCacheServiceDep = Annotated[
    FavoriteMovieCacheService,
    Depends(
        get_favorite_movie_cache_service,
    ),
]

ReviewCacheServiceDep = Annotated[
    ReviewCacheService,
    Depends(get_review_cache_service),
]

UserCacheServiceDep = Annotated[
    UserCacheService,
    Depends(
        get_user_cache_service,
    ),
]

WatchHistoryCacheServiceDep = Annotated[
    WatchHistoryCacheService,
    Depends(
        get_watch_history_cache_service,
    ),
]
