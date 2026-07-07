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
from dependencies.cache_services import (
    get_favorite_movie_cache_service,
    get_genre_cache_service,
    get_movie_cache_service,
    get_review_cache_service,
    get_user_cache_service,
    get_watch_history_cache_service,
)

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
