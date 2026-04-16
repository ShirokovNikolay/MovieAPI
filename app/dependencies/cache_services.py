from typing import Annotated

from fastapi import Depends

from cache_services import GenreCacheService, MovieCacheService
from dependencies.redis_client import (
    get_redis_client_for_genres,
    get_redis_client_for_movies,
)
from dependencies.services import get_genre_service, get_movie_service
from redis_cache import CacheService
from redis_client import RedisClient
from services import GenreService, MovieService


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


async def get_cache_service_for_movies(
    redis: Annotated[
        RedisClient,
        Depends(get_redis_client_for_movies),
    ],
):
    try:
        movie_cache_service = CacheService(redis)
        yield movie_cache_service
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


async def get_movie_cache_service(
    movie_service: Annotated[
        MovieService,
        Depends(get_movie_service),
    ],
    cache_service: Annotated[
        CacheService,
        Depends(get_cache_service_for_movies),
    ],
):
    try:
        movie_cache_service = MovieCacheService(movie_service, cache_service)
        yield movie_cache_service
    finally:
        """
        Действия после view.
        """
