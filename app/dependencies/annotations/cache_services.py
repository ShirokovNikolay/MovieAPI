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
from core.redis import CacheService
from dependencies.cache_services import (
    get_favorite_movie_cache_service,
    get_genre_cache_service,
    get_movie_cache_service,
    get_review_cache_service,
    get_user_cache_service,
    get_watch_history_cache_service,
)
from dependencies.caching import (
    get_cache_service_for_favorite_movies,
    get_cache_service_for_genres,
    get_cache_service_for_movies,
    get_cache_service_for_reviews,
    get_cache_service_for_users,
    get_cache_service_for_watch_history,
)

CacheServiceForGenresDep = Annotated[
    CacheService,
    Depends(get_cache_service_for_genres),
]

CacheServiceForMoviesDep = Annotated[
    CacheService,
    Depends(get_cache_service_for_movies),
]

CacheServiceForFavoriteMoviesDep = Annotated[
    CacheService,
    Depends(
        get_cache_service_for_favorite_movies,
    ),
]

CacheServiceForReviewsDep = Annotated[
    CacheService,
    Depends(
        get_cache_service_for_reviews,
    ),
]

CacheServiceForUsersDep = Annotated[
    CacheService,
    Depends(
        get_cache_service_for_users,
    ),
]

CacheServiceForWatchHistoryDep = Annotated[
    CacheService,
    Depends(
        get_cache_service_for_watch_history,
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
