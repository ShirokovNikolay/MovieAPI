import asyncio
from typing import cast

from core.redis.cache_key_service import CacheKeyService
from core.redis.service import RedisService
from schemas.genre import (
    GenreCreate,
    GenrePartialUpdate,
    GenreResponse,
    GenreResponseList,
    GenreUpdate,
)
from services import GenreService


class GenreCacheService:
    def __init__(
        self,
        genre_service: GenreService,
        redis_service: RedisService,
        cache_key_service: CacheKeyService,
    ) -> None:
        self.genre_service = genre_service
        self.redis_service = redis_service
        self.cache_key_service = cache_key_service

    async def get_genre_by_id(self, genre_id: int) -> GenreResponse:
        key = self.cache_key_service.build_item_key(
            entity="genre",
            entity_id=genre_id,
            action="get",
        )
        cached_genre_response = await self.redis_service.get(key, GenreResponse)
        if cached_genre_response is not None:
            return cast(GenreResponse, cached_genre_response)

        genre_response = await self.genre_service.get_genre_by_id(genre_id)
        await self.redis_service.set(key, genre_response, ttl=24 * 60 * 60)
        return genre_response

    async def get_all_genres(
        self,
        size: int = 10,
        page: int = 1,
    ) -> GenreResponseList:
        key = await self.cache_key_service.build_list_key(
            entity="genre",
            action="get",
            size=size,
            page=page,
        )
        cached_genres_response = await self.redis_service.get(key, GenreResponseList)
        if cached_genres_response is not None:
            return cast(GenreResponseList, cached_genres_response)

        genres_response = await self.genre_service.get_all_genres(size, page)
        await self.redis_service.set(key, genres_response, ttl=24 * 60 * 60)
        return genres_response

    async def search_genres_by_name(
        self,
        search_query: str,
        size: int = 10,
        page: int = 1,
    ) -> GenreResponseList:
        key = await self.cache_key_service.build_list_key(
            entity="genre",
            action="get",
            search_query=search_query,
            size=size,
            page=page,
        )
        cached_genres_response = await self.redis_service.get(key, GenreResponseList)
        if cached_genres_response is not None:
            return cast(GenreResponseList, cached_genres_response)

        genres_response = await self.genre_service.search_genres_by_name(
            search_query,
            size,
            page,
        )
        await self.redis_service.set(key, genres_response, ttl=24 * 60 * 60)
        return genres_response

    async def create_genre(self, create_data: GenreCreate) -> GenreResponse:
        genre_response = await self.genre_service.create_genre(create_data)
        await self.cache_key_service.invalidate_list_keys(entity="genre")
        return genre_response

    async def update_genre(
        self,
        genre_id: int,
        update_data: GenreUpdate,
    ) -> GenreResponse:
        genre_response = await self.genre_service.update_genre(genre_id, update_data)
        key = self.cache_key_service.build_item_key(
            entity="genre",
            entity_id=genre_response.id,
            action="get",
        )
        await asyncio.gather(
            self.cache_key_service.invalidate_list_keys(entity="genre"),
            self.redis_service.delete(key=key),
        )
        return genre_response

    async def partial_update_genre(
        self,
        genre_id: int,
        update_data: GenrePartialUpdate,
    ) -> GenreResponse:
        genre_response = await self.genre_service.partial_update_genre(
            genre_id,
            update_data,
        )
        key = self.cache_key_service.build_item_key(
            entity="genre",
            entity_id=genre_response.id,
            action="get",
        )
        await asyncio.gather(
            self.cache_key_service.invalidate_list_keys(entity="genre"),
            self.redis_service.delete(key=key),
        )
        return genre_response

    async def delete_genre_by_id(self, genre_id: int) -> None:
        await self.genre_service.delete_genre_by_id(genre_id)
        key = self.cache_key_service.build_item_key(
            entity="genre",
            entity_id=genre_id,
            action="get",
        )
        await asyncio.gather(
            self.cache_key_service.invalidate_list_keys(entity="genre"),
            self.redis_service.delete(key=key),
        )
