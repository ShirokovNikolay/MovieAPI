from typing import cast

from core.security.cache_utils import create_cache_key
from core.redis.cache_service import CacheService
from schemas.favorite_movie import (
    FavoriteMovieResponseList,
    FavoriteMovieResponse,
    FavoriteMovieCreate,
)
from services import FavoriteMovieService


class FavoriteMovieCacheService:
    def __init__(
        self,
        favorite_movie_service: FavoriteMovieService,
        cache_service: CacheService,
    ):
        self.favorite_movie_service = favorite_movie_service
        self.cache_service = cache_service

    async def get_favorite_movies_by_user_id(
        self,
        user_id: int,
        size: int = 10,
        page: int = 1,
    ) -> FavoriteMovieResponseList:
        key = create_cache_key(
            "favorite movies",
            user_id=user_id,
            size=size,
            page=page,
        )
        cached_favorite_movies_response = await self.cache_service.get(
            key, FavoriteMovieResponseList
        )
        if cached_favorite_movies_response is not None:
            return cast(FavoriteMovieResponseList, cached_favorite_movies_response)

        favorite_movies_response = (
            await self.favorite_movie_service.get_favorite_movies_by_user_id(
                user_id=user_id,
                page=page,
                size=size,
            )
        )

        await self.cache_service.set(
            key,
            favorite_movies_response,
            ttl=1800,
        )
        return favorite_movies_response

    async def get_favorite_movie_by_id(
        self,
        favorite_movie_id: int,
    ) -> FavoriteMovieResponse:
        key = create_cache_key("favorite movie", favorite_movie_id=favorite_movie_id)
        cached_favorite_movie_response = await self.cache_service.get(
            key, FavoriteMovieResponse
        )
        if cached_favorite_movie_response is not None:
            return cast(FavoriteMovieResponse, cached_favorite_movie_response)

        favorite_movie_response = (
            await self.favorite_movie_service.get_favorite_movie_by_id(
                favorite_movie_id
            )
        )
        await self.cache_service.set(key, favorite_movie_response, ttl=1800)
        return favorite_movie_response

    async def count_favorites_by_movie(self, movie_id: int) -> int:
        key = create_cache_key("favorite movie:count", movie_id=movie_id)
        cached_favorite_movie_response = await self.cache_service.get(key)
        if cached_favorite_movie_response is not None:
            return cast(int, cached_favorite_movie_response)

        favorite_movie_response = (
            await self.favorite_movie_service.count_favorites_by_movie(movie_id)
        )
        await self.cache_service.set(key, favorite_movie_response, ttl=1800)
        return favorite_movie_response

    async def create_user_favorite_movie(
        self,
        user_id: int,
        create_favorite_movie_data: FavoriteMovieCreate,
    ) -> FavoriteMovieResponse:
        favorite_movie_response = (
            await self.favorite_movie_service.create_user_favorite_movie(
                user_id,
                create_favorite_movie_data,
            )
        )
        key = create_cache_key(
            "favorite movie",
        )
        pattern = key + "*"
        await self.cache_service.delete_by_pattern(pattern)
        return favorite_movie_response

    async def delete_favorite_movie_by_id(self, favorite_movie_id: int) -> None:
        await self.favorite_movie_service.delete_favorite_movie_by_id(favorite_movie_id)
        key = create_cache_key(
            "favorite movie",
        )
        pattern = key + "*"
        await self.cache_service.delete_by_pattern(pattern)

    async def delete_user_favorite_movie(self, user_id: int, movie_id: int) -> None:
        await self.favorite_movie_service.delete_user_favorite_movie(user_id, movie_id)
        key = create_cache_key(
            "favorite movie",
        )
        pattern = key + "*"
        await self.cache_service.delete_by_pattern(pattern)
