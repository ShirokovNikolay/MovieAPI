import asyncio
from typing import cast

from core.constants import CacheEntity
from core.redis.cache_key_service import CacheKeyService
from core.redis.service import RedisService
from schemas.favorite_movie import (
    FavoriteMovieCreate,
    FavoriteMovieResponse,
    FavoriteMovieWithMovieResponse,
    FavoriteMovieWithMovieResponseList,
)
from services import FavoriteMovieService


class FavoriteMovieCacheService:
    def __init__(
        self,
        favorite_movie_service: FavoriteMovieService,
        redis_service: RedisService,
        cache_key_service: CacheKeyService,
    ) -> None:
        self.favorite_movie_service = favorite_movie_service
        self.redis_service = redis_service
        self.cache_key_service = cache_key_service

    async def get_favorite_movies_by_user_id(
        self,
        user_id: int,
        size: int = 10,
        page: int = 1,
    ) -> FavoriteMovieWithMovieResponseList:
        key = await self.cache_key_service.build_list_key(
            entity=CacheEntity.favorite_movie,
            action="get",
            version_params={"user_id": user_id},
            user_id=user_id,
            page=page,
            size=size,
        )
        cached_favorite_movies_response = await self.redis_service.get(
            key,
            FavoriteMovieWithMovieResponseList,
        )
        if cached_favorite_movies_response is not None:
            return cast(
                FavoriteMovieWithMovieResponseList,
                cached_favorite_movies_response,
            )

        favorite_movies_response = (
            await self.favorite_movie_service.get_favorite_movies_by_user_id(
                user_id=user_id,
                page=page,
                size=size,
            )
        )

        await self.redis_service.set(
            key,
            favorite_movies_response,
            ttl=24 * 60 * 60,
        )
        return favorite_movies_response

    async def get_favorite_movie_by_id(
        self,
        favorite_movie_id: int,
    ) -> FavoriteMovieWithMovieResponse:
        key = self.cache_key_service.build_item_key(
            entity=CacheEntity.favorite_movie,
            entity_id=favorite_movie_id,
            action="get",
        )
        cached_favorite_movie_response = await self.redis_service.get(
            key,
            FavoriteMovieWithMovieResponse,
        )
        if cached_favorite_movie_response is not None:
            return cast(FavoriteMovieWithMovieResponse, cached_favorite_movie_response)

        favorite_movie_response = (
            await self.favorite_movie_service.get_favorite_movie_by_id(
                favorite_movie_id,
            )
        )
        await self.redis_service.set(
            key,
            favorite_movie_response,
            ttl=5 * 60,
        )
        return favorite_movie_response

    async def count_favorites_by_movie(self, movie_id: int) -> int:
        key = self.cache_key_service.build_item_key(
            entity=CacheEntity.favorite_movie,
            entity_id=movie_id,
            action="get-count",
        )
        cached_favorite_movie_response = await self.redis_service.get(key)
        if cached_favorite_movie_response is not None:
            return cast(int, cached_favorite_movie_response)

        favorite_movie_response = (
            await self.favorite_movie_service.count_favorites_by_movie(movie_id)
        )
        await self.redis_service.set(
            key,
            favorite_movie_response,
            ttl=24 * 60 * 60,
        )
        return favorite_movie_response

    async def check_favorite_movie_status(self, user_id: int, movie_id: int) -> bool:
        entity_id = (user_id, movie_id)
        key = self.cache_key_service.build_item_key(
            entity=CacheEntity.favorite_movie,
            entity_id=entity_id,
            action="get-status",
        )
        cached_favorite_movie_response = await self.redis_service.get(
            key,
            is_boolean=True,
        )
        if cached_favorite_movie_response is not None:
            return cast(bool, cached_favorite_movie_response)

        favorite_movie_response = (
            await self.favorite_movie_service.check_favorite_movie_status(
                user_id,
                movie_id,
            )
        )
        await self.redis_service.set(
            key,
            favorite_movie_response,
            ttl=24 * 60 * 60,
        )
        return favorite_movie_response

    async def create_user_favorite_movie(
        self,
        user_id: int,
        create_favorite_movie_data: FavoriteMovieCreate,
    ) -> FavoriteMovieWithMovieResponse:
        favorite_movie_response = (
            await self.favorite_movie_service.create_user_favorite_movie(
                user_id,
                create_favorite_movie_data,
            )
        )

        movie_id = favorite_movie_response.movie_id
        entity_id = (user_id, movie_id)
        favorite_movie_status_key = self.cache_key_service.build_item_key(
            entity=CacheEntity.favorite_movie,
            entity_id=entity_id,
            action="get-status",
        )
        count_favorite_movie_key = self.cache_key_service.build_item_key(
            entity=CacheEntity.favorite_movie,
            entity_id=movie_id,
            action="get-count",
        )
        await asyncio.gather(
            self.cache_key_service.invalidate_list_keys(
                entity=CacheEntity.favorite_movie,
                user_id=user_id,
            ),
            self.redis_service.delete(favorite_movie_status_key),
            self.redis_service.incr_by(
                count_favorite_movie_key,
                amount=1,
            ),
        )
        return favorite_movie_response

    async def delete_favorite_movie_by_id(
        self,
        user_id: int,
        favorite_movie_id: int,
    ) -> FavoriteMovieResponse:
        favorite_movie = await self.favorite_movie_service.delete_favorite_movie_by_id(
            user_id,
            favorite_movie_id,
        )

        movie_id = favorite_movie.movie_id
        entity_id = (user_id, movie_id)
        favorite_movie_status_key = self.cache_key_service.build_item_key(
            entity=CacheEntity.favorite_movie,
            entity_id=entity_id,
            action="get-status",
        )
        count_favorite_movie_key = self.cache_key_service.build_item_key(
            entity=CacheEntity.favorite_movie,
            entity_id=movie_id,
            action="get-count",
        )
        await asyncio.gather(
            self.cache_key_service.invalidate_list_keys(
                entity=CacheEntity.favorite_movie,
                user_id=user_id,
            ),
            self.redis_service.delete(favorite_movie_status_key),
            self.redis_service.incr_by(
                count_favorite_movie_key,
                amount=-1,
            ),
        )
        return favorite_movie

    async def delete_user_favorite_movie(
        self,
        user_id: int,
        movie_id: int,
    ) -> FavoriteMovieResponse:
        favorite_movie = await self.favorite_movie_service.delete_user_favorite_movie(
            user_id,
            movie_id,
        )

        entity_id = (user_id, movie_id)
        favorite_movie_status_key = self.cache_key_service.build_item_key(
            entity=CacheEntity.favorite_movie,
            entity_id=entity_id,
            action="get-status",
        )
        count_favorite_movie_key = self.cache_key_service.build_item_key(
            entity=CacheEntity.favorite_movie,
            entity_id=movie_id,
            action="get-count",
        )
        await asyncio.gather(
            self.cache_key_service.invalidate_list_keys(
                entity=CacheEntity.favorite_movie,
                user_id=user_id,
            ),
            self.redis_service.delete(favorite_movie_status_key),
            self.redis_service.incr_by(
                count_favorite_movie_key,
                amount=-1,
            ),
        )
        return favorite_movie
