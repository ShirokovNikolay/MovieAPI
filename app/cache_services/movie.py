import asyncio
from typing import cast

from core.constants import CacheEntity
from core.redis.cache_key_service import CacheKeyService
from core.redis.service import RedisService
from dependencies.annotations.validators import PaginationPageDep, PaginationSizeDep
from schemas.movie import (
    MovieCreate,
    MovieFilter,
    MoviePartialUpdate,
    MovieResponseList,
    MovieUpdate,
    MovieWithGenreResponse,
    MovieWithGenreResponseList,
)
from schemas.watch_history import WatchHistoryCreate
from services import MovieService


class MovieCacheService:
    def __init__(
        self,
        movie_service: MovieService,
        movie_redis_service: RedisService,
        watch_history_redis_service: RedisService,
        cache_key_service: CacheKeyService,
    ) -> None:
        self.movie_service = movie_service
        self.movie_redis_service = movie_redis_service
        self.watch_history_redis_service = watch_history_redis_service
        self.cache_key_service = cache_key_service

    async def get_movie_by_id(self, movie_id: int) -> MovieWithGenreResponse:
        key = self.cache_key_service.build_item_key(
            entity=CacheEntity.movie,
            entity_id=movie_id,
            action="get",
        )
        cached_movie_response = await self.movie_redis_service.get(
            key,
            MovieWithGenreResponse,
        )
        if cached_movie_response is not None:
            return cast(MovieWithGenreResponse, cached_movie_response)

        movie_response = await self.movie_service.get_movie_by_id(movie_id)
        await self.movie_redis_service.set(
            key,
            movie_response,
            ttl=24 * 60 * 60,
        )
        return movie_response

    async def get_movies(
        self,
        size: int = 10,
        page: int = 1,
    ) -> MovieWithGenreResponseList:
        key = await self.cache_key_service.build_list_key(
            entity=CacheEntity.movie,
            action="get",
            size=size,
            page=page,
        )
        cached_movies_response = await self.movie_redis_service.get(
            key,
            MovieWithGenreResponseList,
        )
        if cached_movies_response is not None:
            return cast(MovieWithGenreResponseList, cached_movies_response)

        movies_response = await self.movie_service.get_movies(size, page)
        await self.movie_redis_service.set(
            key,
            movies_response,
            ttl=24 * 60 * 60,
        )
        return movies_response

    async def search_movies_with_filters(
        self,
        movie_filter: MovieFilter,
        size: PaginationSizeDep = 10,
        page: PaginationPageDep = 1,
    ) -> MovieWithGenreResponseList:
        key = await self.cache_key_service.build_list_key(
            entity=CacheEntity.movie,
            action="get-search",
            size=size,
            page=page,
            **movie_filter.model_dump(),
        )
        cached_movies_response = await self.movie_redis_service.get(
            key,
            MovieWithGenreResponseList,
        )
        if cached_movies_response is not None:
            return cast(MovieWithGenreResponseList, cached_movies_response)

        movies_response = await self.movie_service.search_movies_with_filters(
            movie_filter,
            size,
            page,
        )
        await self.movie_redis_service.set(
            key,
            movies_response,
            ttl=24 * 60 * 60,
        )
        return movies_response

    async def get_movies_by_genre_id(
        self,
        genre_id: int,
    ) -> MovieResponseList:
        key = await self.cache_key_service.build_list_key(
            entity=CacheEntity.movie,
            action="get-search",
            genre_id=genre_id,
        )
        cached_movies_response = await self.movie_redis_service.get(
            key,
            MovieResponseList,
        )
        if cached_movies_response is not None:
            return cast(MovieResponseList, cached_movies_response)

        movies_response = await self.movie_service.get_movies_by_genre_id(
            genre_id,
        )
        await self.movie_redis_service.set(
            key,
            movies_response,
            ttl=24 * 60 * 60,
        )
        return movies_response

    async def watch_movie(
        self,
        user_id: int,
        create_watch_history_data: WatchHistoryCreate,
    ) -> MovieWithGenreResponse:
        movie_response = await self.movie_service.watch_movie(
            user_id,
            create_watch_history_data,
        )
        count_watch_history_key = self.cache_key_service.build_item_key(
            entity=CacheEntity.watch_history,
            entity_id=user_id,
            action="get-count",
        )
        await asyncio.gather(
            self.watch_history_redis_service.incr_by(
                count_watch_history_key,
                amount=1,
            ),
            self.cache_key_service.invalidate_list_keys(
                entity=CacheEntity.watch_history,
                user_id=user_id,
            ),
        )
        return movie_response

    async def create_movie(
        self,
        create_movie_data: MovieCreate,
    ) -> MovieWithGenreResponse:
        movie_response = await self.movie_service.create_movie(create_movie_data)
        await self.cache_key_service.invalidate_list_keys(entity=CacheEntity.movie)
        return movie_response

    async def update_movie(
        self,
        movie_id: int,
        update_movie_data: MovieUpdate,
    ) -> MovieWithGenreResponse:
        movie_response = await self.movie_service.update_movie(
            movie_id,
            update_movie_data,
        )
        movie_key = self.cache_key_service.build_item_key(
            entity=CacheEntity.movie,
            entity_id=movie_id,
            action="get",
        )
        await asyncio.gather(
            self.cache_key_service.invalidate_list_keys(entity=CacheEntity.movie),
            self.movie_redis_service.delete(movie_key),
        )
        return movie_response

    async def partial_update_movie(
        self,
        movie_id: int,
        update_movie_data: MoviePartialUpdate,
    ) -> MovieWithGenreResponse:
        movie_response = await self.movie_service.partial_update_movie(
            movie_id,
            update_movie_data,
        )
        movie_key = self.cache_key_service.build_item_key(
            entity=CacheEntity.movie,
            entity_id=movie_id,
            action="get",
        )
        await asyncio.gather(
            self.cache_key_service.invalidate_list_keys(entity=CacheEntity.movie),
            self.movie_redis_service.delete(movie_key),
        )
        return movie_response

    async def delete_movie_by_id(self, movie_id: int) -> None:
        await self.movie_service.delete_movie_by_id(movie_id)
        movie_key = self.cache_key_service.build_item_key(
            entity=CacheEntity.movie,
            entity_id=movie_id,
            action="get",
        )
        await asyncio.gather(
            self.cache_key_service.invalidate_list_keys(entity=CacheEntity.movie),
            self.movie_redis_service.delete(movie_key),
        )
