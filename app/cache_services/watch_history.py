from datetime import datetime
from typing import cast

from core.redis.cache_service import CacheService
from core.security.cache_utils import create_cache_key
from schemas.watch_history import (
    WatchHistoryResponse,
    WatchHistoryResponseList,
)
from services import WatchHistoryService


class WatchHistoryCacheService:
    def __init__(
        self,
        watch_history_service: WatchHistoryService,
        cache_service: CacheService,
    ) -> None:
        self.watch_history_service = watch_history_service
        self.cache_service = cache_service

    async def get_watch_history_by_id(
        self,
        watch_history_id: int,
    ) -> WatchHistoryResponse:
        key = create_cache_key(
            "watch_history",
            watch_history_id=watch_history_id,
        )
        cached_watch_history_response = await self.cache_service.get(
            key,
            WatchHistoryResponse,
        )
        if cached_watch_history_response is not None:
            return cast(WatchHistoryResponse, cached_watch_history_response)

        watch_history_response = (
            await self.watch_history_service.get_watch_history_by_id(watch_history_id)
        )
        await self.cache_service.set(key, watch_history_response)
        return watch_history_response

    async def get_watch_history_list(
        self,
        user_id: int,
        size: int = 10,
        page: int = 1,
    ) -> WatchHistoryResponseList:
        key = create_cache_key(
            "watch_history_list",
            user_id=user_id,
            size=size,
            page=page,
        )
        cached_watch_history_list_response = await self.cache_service.get(
            key,
            WatchHistoryResponseList,
        )
        if cached_watch_history_list_response is not None:
            return cast(WatchHistoryResponseList, cached_watch_history_list_response)

        watch_history_list_response = (
            await self.watch_history_service.get_watch_history_list(user_id, size, page)
        )
        await self.cache_service.set(key, watch_history_list_response)
        return watch_history_list_response

    async def get_watch_history_by_date_range(
        self,
        user_id: int,
        start_date: datetime,
        end_date: datetime,
        size: int = 10,
        page: int = 1,
    ) -> WatchHistoryResponseList:
        key = create_cache_key(
            "watch_history_list",
            user_id=user_id,
            start_date=start_date,
            end_date=end_date,
            size=size,
            page=page,
        )
        cached_watch_history_list_response = await self.cache_service.get(
            key,
            WatchHistoryResponseList,
        )
        if cached_watch_history_list_response is not None:
            return cast(WatchHistoryResponseList, cached_watch_history_list_response)

        watch_history_list_response = (
            await self.watch_history_service.get_watch_history_by_date_range(
                user_id,
                start_date,
                end_date,
                size,
                page,
            )
        )
        await self.cache_service.set(key, watch_history_list_response)
        return watch_history_list_response

    async def count_user_watch_history(self, user_id: int) -> int:
        key = create_cache_key("watch_history", user_id=user_id)
        cached_watch_history_response = await self.cache_service.get(key)
        if cached_watch_history_response is not None:
            return cast(int, cached_watch_history_response)
        watch_history_response = (
            await self.watch_history_service.count_user_watch_history(user_id)
        )
        await self.cache_service.set(key, watch_history_response)
        return watch_history_response

    async def delete_watch_history_by_id(self, watch_history_id: int) -> None:
        await self.watch_history_service.delete_watch_history_by_id(watch_history_id)
        key = create_cache_key("watch_history")
        pattern = key + "*"
        await self.cache_service.delete_by_pattern(pattern)

    async def delete_user_watch_history(self, user_id: int) -> None:
        await self.watch_history_service.delete_user_watch_history(user_id)
        key = create_cache_key("watch_history")
        pattern = key + "*"
        await self.cache_service.delete_by_pattern(pattern)
