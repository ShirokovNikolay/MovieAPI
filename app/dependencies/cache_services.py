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
from core.redis.cache_service import CacheService
from dependencies.caching import (
    get_cache_service_for_favorite_movies,
    get_cache_service_for_genres,
    get_cache_service_for_movies,
    get_cache_service_for_reviews,
    get_cache_service_for_users,
    get_cache_service_for_watch_history,
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
    cache_service: Annotated[
        CacheService,
        Depends(get_cache_service_for_genres),
    ],
) -> AsyncGenerator[GenreCacheService]:
    try:
        genre_cache_service = GenreCacheService(genre_service, cache_service)
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
    cache_service_for_movie: Annotated[
        CacheService,
        Depends(get_cache_service_for_movies),
    ],
    cache_service_for_watch_history: Annotated[
        CacheService,
        Depends(get_cache_service_for_watch_history),
    ],
) -> AsyncGenerator[MovieCacheService]:
    try:
        movie_cache_service = MovieCacheService(
            movie_service,
            cache_service_for_movie,
            cache_service_for_watch_history,
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
    cache_service: Annotated[
        CacheService,
        Depends(get_cache_service_for_favorite_movies),
    ],
) -> AsyncGenerator[FavoriteMovieCacheService]:
    try:
        favorite_movie_cache_service = FavoriteMovieCacheService(
            favorite_movie_service, cache_service,
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
    cache_service: Annotated[
        CacheService,
        Depends(get_cache_service_for_reviews),
    ],
) -> AsyncGenerator[ReviewCacheService]:
    try:
        review_cache_service = ReviewCacheService(review_service, cache_service)
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
    cache_service: Annotated[
        CacheService,
        Depends(get_cache_service_for_watch_history),
    ],
) -> AsyncGenerator[WatchHistoryCacheService]:
    try:
        watch_history_cache_service = WatchHistoryCacheService(
            watch_history_service, cache_service,
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
    cache_service: Annotated[
        CacheService,
        Depends(get_cache_service_for_users),
    ],
) -> AsyncGenerator[UserCacheService]:
    try:
        user_cache_service = UserCacheService(user_service, cache_service)
        yield user_cache_service
    finally:
        """
        Действия после view.
        """
