from core.security.cache_utils import create_cache_key
from core.redis.cache_service import CacheService

from schemas.genre import (
    GenreCreate,
    GenreUpdate,
    GenreResponse,
    GenrePartialUpdate,
    GenreResponseList,
)

from services import GenreService


class GenreCacheService:
    def __init__(
        self,
        genre_service: GenreService,
        cache_service: CacheService,
    ):
        self.genre_service = genre_service
        self.cache_service = cache_service

    async def get_genre_by_id(self, genre_id: int) -> GenreResponse:
        key = create_cache_key("genre", genre_id=genre_id)
        cached_genre_response = await self.cache_service.get(key, GenreResponse)
        if cached_genre_response is not None:
            return cached_genre_response

        genre_response = await self.genre_service.get_genre_by_id(genre_id)
        await self.cache_service.set(key, genre_response, ttl=1800)
        return genre_response

    async def get_all_genres(
        self,
        size: int = 10,
        page: int = 1,
    ) -> GenreResponseList:
        key = create_cache_key(
            "genres",
            size=size,
            page=page,
        )
        cached_genres_response = await self.cache_service.get(key, GenreResponseList)
        if cached_genres_response is not None:
            return cached_genres_response

        genres_response = await self.genre_service.get_all_genres(size, page)
        await self.cache_service.set(key, genres_response, ttl=180)
        return genres_response

    async def search_genres_by_name(
        self,
        name: str,
        size: int = 10,
        page: int = 1,
    ) -> GenreResponseList:
        key = create_cache_key(
            "genres",
            name=name,
            size=size,
            page=page,
        )
        cached_genres_response = await self.cache_service.get(key, GenreResponseList)
        if cached_genres_response is not None:
            return cached_genres_response

        genres_response = await self.genre_service.search_genres_by_name(
            name,
            size,
            page,
        )
        await self.cache_service.set(key, genres_response, ttl=180)
        return genres_response

    async def create_genre(self, create_data: GenreCreate) -> GenreResponse:
        genre_response = await self.genre_service.create_genre(create_data)
        key = create_cache_key("genre")
        pattern = key + "*"
        await self.cache_service.delete_by_pattern(pattern)
        return genre_response

    async def update_genre(
        self, genre_id: int, update_data: GenreUpdate
    ) -> GenreResponse:
        genre_response = await self.genre_service.update_genre(genre_id, update_data)
        key = create_cache_key("genre")
        pattern = key + "*"
        await self.cache_service.delete_by_pattern(pattern)
        return genre_response

    async def partial_update_genre(
        self, genre_id: int, update_data: GenrePartialUpdate
    ) -> GenreResponse:
        genre_response = await self.genre_service.partial_update_genre(
            genre_id, update_data
        )
        key = create_cache_key("genre")
        pattern = key + "*"
        await self.cache_service.delete_by_pattern(pattern)
        return genre_response

    async def delete_genre_by_id(self, genre_id: int) -> None:
        await self.genre_service.delete_genre_by_id(genre_id)
        key = create_cache_key("genre")
        pattern = key + "*"
        await self.cache_service.delete_by_pattern(pattern)
