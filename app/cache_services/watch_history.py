import asyncio
from datetime import date
from typing import cast

from core.constants import CacheEntity
from core.redis.cache_key_service import CacheKeyService
from core.redis.service import RedisService
from schemas.watch_history import (
    WatchHistoryCreate,
    WatchHistoryWithMovieResponse,
    WatchHistoryWithMovieResponseList,
)
from services import WatchHistoryService


class WatchHistoryCacheService:
    def __init__(
        self,
        watch_history_service: WatchHistoryService,
        cache_service: RedisService,
        cache_key_service: CacheKeyService,
    ) -> None:
        self.watch_history_service = watch_history_service
        self.cache_service = cache_service
        self.cache_key_service = cache_key_service

    async def get_watch_history_by_id(
        self,
        watch_history_id: int,
    ) -> WatchHistoryWithMovieResponse:
        key = self.cache_key_service.build_item_key(
            entity=CacheEntity.watch_history,
            entity_id=watch_history_id,
            action="get",
        )
        cached_watch_history_response = await self.cache_service.get(
            key,
            schema=WatchHistoryWithMovieResponse,
        )
        if cached_watch_history_response is not None:
            return cast(WatchHistoryWithMovieResponse, cached_watch_history_response)

        watch_history_response = (
            await self.watch_history_service.get_watch_history_by_id(watch_history_id)
        )
        await self.cache_service.set(
            key,
            watch_history_response,
            ttl=5 * 60,
        )
        return watch_history_response

    async def get_watch_history_list(
        self,
        user_id: int,
        size: int = 10,
        page: int = 1,
    ) -> WatchHistoryWithMovieResponseList:
        key = await self.cache_key_service.build_list_key(
            entity=CacheEntity.watch_history,
            action="get",
            user_id=user_id,
            size=size,
            page=page,
        )
        cached_watch_history_list_response = await self.cache_service.get(
            key,
            WatchHistoryWithMovieResponseList,
        )
        if cached_watch_history_list_response is not None:
            return cast(
                WatchHistoryWithMovieResponseList,
                cached_watch_history_list_response,
            )

        watch_history_list_response = (
            await self.watch_history_service.get_watch_history_list(user_id, size, page)
        )
        await self.cache_service.set(
            key,
            watch_history_list_response,
            ttl=15 * 60,
        )
        return watch_history_list_response

    async def get_watch_history_by_date_range(
        self,
        user_id: int,
        start_date: date,
        end_date: date,
        size: int = 10,
        page: int = 1,
    ) -> WatchHistoryWithMovieResponseList:
        key = await self.cache_key_service.build_list_key(
            entity=CacheEntity.watch_history,
            action="get",
            user_id=user_id,
            start_date=start_date,
            end_date=end_date,
            size=size,
            page=page,
        )
        cached_watch_history_list_response = await self.cache_service.get(
            key,
            WatchHistoryWithMovieResponseList,
        )
        if cached_watch_history_list_response is not None:
            return cast(
                WatchHistoryWithMovieResponseList,
                cached_watch_history_list_response,
            )

        watch_history_list_response = (
            await self.watch_history_service.get_watch_history_by_date_range(
                user_id,
                start_date,
                end_date,
                size,
                page,
            )
        )
        await self.cache_service.set(
            key,
            watch_history_list_response,
            ttl=15 * 60,
        )
        return watch_history_list_response

    async def count_user_watch_history(self, user_id: int) -> int:
        key = self.cache_key_service.build_item_key(
            entity=CacheEntity.watch_history,
            entity_id=user_id,
            action="get-count",
        )
        cached_watch_history_response = await self.cache_service.get(key)
        if cached_watch_history_response is not None:
            return cast(int, cached_watch_history_response)
        watch_history_response = (
            await self.watch_history_service.count_user_watch_history(user_id)
        )
        await self.cache_service.set(
            key,
            watch_history_response,
            ttl=24 * 60 * 60,
        )
        return watch_history_response

    async def add_movie_to_watch_history(
        self,
        user_id: int,
        create_watch_history_data: WatchHistoryCreate,
    ) -> WatchHistoryWithMovieResponse: ...

    async def delete_watch_history_by_id(
        self,
        user_id: int,
        watch_history_id: int,
    ) -> None:
        watch_history_count_key = self.cache_key_service.build_item_key(
            entity=CacheEntity.watch_history,
            entity_id=user_id,
            action="get-count",
        )
        watch_history_key = self.cache_key_service.build_item_key(
            entity=CacheEntity.watch_history,
            entity_id=watch_history_id,
            action="get",
        )
        user_watch_history_pattern_coroutine = (
            self.cache_key_service.build_list_regex_key(
                entity=CacheEntity.watch_history,
                action_regex="get",
                user_id=user_id,
                size="*",
                page="*",
            )
        )
        user_watch_history_range_date_pattern_coroutine = (
            self.cache_key_service.build_list_key(
                entity=CacheEntity.watch_history,
                action="get",
                user_id=user_id,
                start_date="*",
                end_date="*",
                size="*",
                page="*",
            )
        )
        user_watch_history_pattern, user_watch_history_range_date_pattern = (
            await asyncio.gather(
                user_watch_history_pattern_coroutine,
                user_watch_history_range_date_pattern_coroutine,
            )
        )

        delete_watch_history_item = (
            self.watch_history_service.delete_watch_history_by_id(
                user_id,
                watch_history_id,
            )
        )
        change_watch_history_count_cache = self.cache_service.incr_by(
            key=watch_history_count_key,
            amount=-1,
        )
        delete_watch_history_item_cache = self.cache_service.delete(watch_history_key)
        delete_watch_history_cache = self.cache_service.delete_by_pattern(
            user_watch_history_pattern,
        )
        delete_watch_history_range_date_cache = self.cache_service.delete_by_pattern(
            user_watch_history_range_date_pattern,
        )
        await asyncio.gather(
            delete_watch_history_item,
            change_watch_history_count_cache,
            delete_watch_history_item_cache,
            delete_watch_history_cache,
            delete_watch_history_range_date_cache,
        )

    async def delete_user_watch_history(self, user_id: int) -> None:
        await self.watch_history_service.delete_user_watch_history(user_id)

        watch_history_count_key = self.cache_key_service.build_item_key(
            entity=CacheEntity.watch_history,
            entity_id=user_id,
            action="get-count",
        )
        user_watch_history_pattern_coroutine = (
            self.cache_key_service.build_list_regex_key(
                entity=CacheEntity.watch_history,
                action_regex="get",
                user_id=user_id,
                size="*",
                page="*",
            )
        )
        user_watch_history_range_date_pattern_coroutine = (
            self.cache_key_service.build_list_key(
                entity=CacheEntity.watch_history,
                action="get",
                user_id=user_id,
                start_date="*",
                end_date="*",
                size="*",
                page="*",
            )
        )
        user_watch_history_pattern, user_watch_history_range_date_pattern = (
            await asyncio.gather(
                user_watch_history_pattern_coroutine,
                user_watch_history_range_date_pattern_coroutine,
            )
        )

        delete_watch_history_count_cache = self.cache_service.delete(
            key=watch_history_count_key,
        )
        delete_watch_history_cache = self.cache_service.delete_by_pattern(
            user_watch_history_pattern,
        )
        delete_watch_history_range_date_cache = self.cache_service.delete_by_pattern(
            user_watch_history_range_date_pattern,
        )
        await asyncio.gather(
            delete_watch_history_count_cache,
            delete_watch_history_cache,
            delete_watch_history_range_date_cache,
        )
