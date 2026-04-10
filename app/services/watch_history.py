from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from core.exceptions.user import UserIdNotFoundError
from core.exceptions.watch_history import WatchHistoryIdNotFoundError
from repositories import UserRepository
from repositories.watch_history import WatchHistoryRepository
from schemas.watch_history import (
    WatchHistoryResponse,
    WatchHistoryResponseList,
    WatchHistoryCreate,
)


class WatchHistoryService:
    def __init__(self, session: AsyncSession):
        self.user_repository = UserRepository(session)
        self.watch_history_repository = WatchHistoryRepository(session)

    async def get_watch_history_by_id(
        self, watch_history_id: int
    ) -> WatchHistoryResponse:
        watch_history = await self.watch_history_repository.get_watch_history_by_id(
            watch_history_id
        )
        if watch_history is not None:
            return WatchHistoryResponse.model_validate(watch_history)
        raise WatchHistoryIdNotFoundError(watch_history_id)

    async def watch_history_exists(self, watch_history_id: int) -> bool:
        return await self.watch_history_repository.watch_history_exists(
            watch_history_id
        )

    async def get_watch_history_list(self, user_id: int) -> WatchHistoryResponseList:
        if await self.user_repository.user_id_exists(user_id):
            watch_history_list = [
                WatchHistoryResponse.model_validate(watch_history)
                for watch_history in await self.watch_history_repository.get_watch_history_list(
                    user_id
                )
            ]
            return WatchHistoryResponseList(watch_history_list=watch_history_list)
        raise UserIdNotFoundError(user_id)

    async def get_watch_history_by_date_range(
        self,
        user_id: int,
        start_date: datetime,
        end_date: datetime,
    ) -> WatchHistoryResponseList:
        if await self.user_repository.user_id_exists(user_id):
            watch_history_list = [
                WatchHistoryResponse.model_validate(watch_history)
                for watch_history in await self.watch_history_repository.get_watch_history_by_date_range(
                    user_id,
                    start_date,
                    end_date,
                )
            ]
            return WatchHistoryResponseList(watch_history_list=watch_history_list)
        raise UserIdNotFoundError(user_id)

    async def count_user_watch_history(self, user_id: int) -> int:
        if await self.user_repository.user_id_exists(user_id):
            return await self.watch_history_repository.count_user_watch_history(user_id)
        raise UserIdNotFoundError(user_id)

    async def add_movie_to_watch_history(
        self,
        user_id: int,
        create_watch_history_data: WatchHistoryCreate,
    ) -> WatchHistoryResponse:
        if await self.user_repository.user_id_exists(user_id):
            watch_history = (
                await self.watch_history_repository.add_movie_to_watch_history(
                    user_id,
                    create_watch_history_data,
                )
            )
            return WatchHistoryResponse.model_validate(watch_history)
        raise UserIdNotFoundError(user_id)

    async def delete_watch_history_by_id(self, watch_history_id: int) -> None:
        if not await self.watch_history_repository.delete_watch_history_by_id(
            watch_history_id
        ):
            raise WatchHistoryIdNotFoundError(watch_history_id)

    async def delete_user_watch_history(self, user_id: int) -> None:
        if not await self.user_repository.user_id_exists(user_id):
            raise UserIdNotFoundError(user_id)
        await self.watch_history_repository.delete_user_watch_history(user_id)
