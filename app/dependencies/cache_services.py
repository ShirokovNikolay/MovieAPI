from collections.abc import AsyncGenerator
from typing import Annotated

from fastapi import Depends

from cache_services import (
    FavoriteMovieCacheService,
    GenreCacheService,
    MovieCacheService,
    ReviewCacheService,
    UserCacheService,
)
from cache_services.watch_history import WatchHistoryCacheService
from core.redis.cache_key_service import CacheKeyService
from core.redis.service import RedisService
from dependencies.cache_key_service import get_cache_key_service
from dependencies.redis_services import (
    get_favorite_movie_redis_service,
    get_genre_redis_service,
    get_movie_redis_service,
    get_review_redis_service,
    get_user_redis_service,
    get_watch_history_redis_service,
)
from dependencies.services import (
    get_favorite_movie_service,
    get_genre_service,
    get_movie_service,
    get_review_service,
    get_user_service,
    get_watch_history_service,
)
from services import (
    FavoriteMovieService,
    GenreService,
    MovieService,
    ReviewService,
    UserService,
    WatchHistoryService,
)


async def get_genre_cache_service(
    genre_service: Annotated[
        GenreService,
        Depends(get_genre_service),
    ],
    genre_redis_service: Annotated[
        RedisService,
        Depends(get_genre_redis_service),
    ],
    cache_key_service: Annotated[
        CacheKeyService,
        Depends(get_cache_key_service),
    ],
) -> AsyncGenerator[GenreCacheService]:
    try:
        genre_cache_service = GenreCacheService(
            genre_service,
            genre_redis_service,
            cache_key_service,
        )
        yield genre_cache_service
    finally:
        """
        Действия после view.
        """


async def get_movie_cache_service(
    movie_service: Annotated[
        MovieService,
        Depends(get_movie_service),
    ],
    movie_redis_service: Annotated[
        RedisService,
        Depends(get_movie_redis_service),
    ],
    watch_history_redis_service: Annotated[
        RedisService,
        Depends(get_watch_history_redis_service),
    ],
    cache_key_service: Annotated[
        CacheKeyService,
        Depends(get_cache_key_service),
    ],
) -> AsyncGenerator[MovieCacheService]:
    try:
        movie_cache_service = MovieCacheService(
            movie_service,
            movie_redis_service,
            watch_history_redis_service,
            cache_key_service,
        )
        yield movie_cache_service
    finally:
        """
        Действия после view.
        """


async def get_favorite_movie_cache_service(
    favorite_movie_service: Annotated[
        FavoriteMovieService,
        Depends(get_favorite_movie_service),
    ],
    favorite_movie_redis_service: Annotated[
        RedisService,
        Depends(get_favorite_movie_redis_service),
    ],
    cache_key_service: Annotated[
        CacheKeyService,
        Depends(get_cache_key_service),
    ],
) -> AsyncGenerator[FavoriteMovieCacheService]:
    try:
        favorite_movie_cache_service = FavoriteMovieCacheService(
            favorite_movie_service,
            favorite_movie_redis_service,
            cache_key_service,
        )
        yield favorite_movie_cache_service
    finally:
        """
        Действия после view.
        """


async def get_review_cache_service(
    review_service: Annotated[
        ReviewService,
        Depends(get_review_service),
    ],
    review_redis_service: Annotated[
        RedisService,
        Depends(get_review_redis_service),
    ],
    cache_key_service: Annotated[
        CacheKeyService,
        Depends(get_cache_key_service),
    ],
) -> AsyncGenerator[ReviewCacheService]:
    try:
        review_cache_service = ReviewCacheService(
            review_service,
            review_redis_service,
            cache_key_service,
        )
        yield review_cache_service
    finally:
        """
        Действия после view.
        """


async def get_watch_history_cache_service(
    watch_history_service: Annotated[
        WatchHistoryService,
        Depends(get_watch_history_service),
    ],
    watch_history_redis_service: Annotated[
        RedisService,
        Depends(get_watch_history_redis_service),
    ],
    cache_key_service: Annotated[
        CacheKeyService,
        Depends(get_cache_key_service),
    ],
) -> AsyncGenerator[WatchHistoryCacheService]:
    try:
        watch_history_cache_service = WatchHistoryCacheService(
            watch_history_service,
            watch_history_redis_service,
            cache_key_service,
        )
        yield watch_history_cache_service
    finally:
        """
        Действия после view.
        """


async def get_user_cache_service(
    user_service: Annotated[
        UserService,
        Depends(get_user_service),
    ],
    user_redis_service: Annotated[
        RedisService,
        Depends(get_user_redis_service),
    ],
    cache_key_service: Annotated[
        CacheKeyService,
        Depends(get_cache_key_service),
    ],
) -> AsyncGenerator[UserCacheService]:
    try:
        user_cache_service = UserCacheService(
            user_service,
            user_redis_service,
            cache_key_service,
        )
        yield user_cache_service
    finally:
        """
        Действия после view.
        """
