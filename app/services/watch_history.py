from datetime import date

from sqlalchemy.ext.asyncio import AsyncSession

from core.exceptions.auth import PermissionDeniedError
from core.exceptions.user import UserIdNotFoundError
from core.exceptions.watch_history import WatchHistoryIdNotFoundError
from repositories import UserRepository
from repositories.watch_history import WatchHistoryRepository
from schemas.user import UserResponse
from schemas.watch_history import (
    WatchHistoryCreate,
    WatchHistoryWithMovieResponse,
    WatchHistoryWithMovieResponseList,
)


class WatchHistoryService:
    def __init__(self, session: AsyncSession) -> None:
        self.user_repository = UserRepository(session)
        self.watch_history_repository = WatchHistoryRepository(session)

    async def get_watch_history_owner(self, watch_history_id: int) -> UserResponse:
        if not self.watch_history_repository.watch_history_exists(watch_history_id):
            raise WatchHistoryIdNotFoundError(watch_history_id)

        user = await self.watch_history_repository.get_watch_history_owner(
            watch_history_id,
        )
        return UserResponse.model_validate(user)

    async def get_watch_history_by_id(
        self,
        watch_history_id: int,
    ) -> WatchHistoryWithMovieResponse:
        watch_history = await self.watch_history_repository.get_watch_history_by_id(
            watch_history_id,
        )
        if watch_history is not None:
            return WatchHistoryWithMovieResponse.model_validate(watch_history)
        raise WatchHistoryIdNotFoundError(watch_history_id)

    async def watch_history_exists(self, watch_history_id: int) -> bool:
        return await self.watch_history_repository.watch_history_exists(
            watch_history_id,
        )

    async def get_watch_history_list(
        self,
        user_id: int,
        size: int = 10,
        page: int = 1,
    ) -> WatchHistoryWithMovieResponseList:
        if not await self.user_repository.user_id_exists(user_id):
            raise UserIdNotFoundError(user_id)

        watch_history_models = (
            await self.watch_history_repository.get_watch_history_list(
                user_id,
                size,
                page,
            )
        )
        watch_history_list = [
            WatchHistoryWithMovieResponse.model_validate(watch_history)
            for watch_history in watch_history_models
        ]
        return WatchHistoryWithMovieResponseList(
            watch_history_list=watch_history_list,
            size=size,
            page=page,
        )

    async def get_watch_history_by_date_range(
        self,
        user_id: int,
        start_date: date,
        end_date: date,
        size: int = 10,
        page: int = 1,
    ) -> WatchHistoryWithMovieResponseList:
        if not await self.user_repository.user_id_exists(user_id):
            raise UserIdNotFoundError(user_id)

        watch_history_models = (
            await self.watch_history_repository.get_watch_history_by_date_range(
                user_id,
                start_date,
                end_date,
                size,
                page,
            )
        )
        watch_history_list = [
            WatchHistoryWithMovieResponse.model_validate(watch_history)
            for watch_history in watch_history_models
        ]
        return WatchHistoryWithMovieResponseList(
            watch_history_list=watch_history_list,
            size=size,
            page=page,
        )

    async def count_user_watch_history(self, user_id: int) -> int:
        if await self.user_repository.user_id_exists(user_id):
            return await self.watch_history_repository.count_user_watch_history(user_id)
        raise UserIdNotFoundError(user_id)

    async def add_movie_to_watch_history(
        self,
        user_id: int,
        create_watch_history_data: WatchHistoryCreate,
    ) -> WatchHistoryWithMovieResponse:
        if not await self.user_repository.user_id_exists(user_id):
            raise UserIdNotFoundError(user_id)

        watch_history = await self.watch_history_repository.add_movie_to_watch_history(
            user_id,
            create_watch_history_data,
        )
        return WatchHistoryWithMovieResponse.model_validate(watch_history)

    async def delete_watch_history_by_id(
        self,
        user_id: int,
        watch_history_id: int,
    ) -> None:
        if not self.user_repository.user_id_exists(user_id):
            raise UserIdNotFoundError(user_id)

        owner = await self.get_watch_history_owner(watch_history_id)
        if owner.id != user_id:
            raise PermissionDeniedError
        if not await self.watch_history_repository.delete_watch_history_by_id(
            watch_history_id,
        ):
            raise WatchHistoryIdNotFoundError(watch_history_id)

    async def delete_user_watch_history(self, user_id: int) -> None:
        if not await self.user_repository.user_id_exists(user_id):
            raise UserIdNotFoundError(user_id)
        await self.watch_history_repository.delete_user_watch_history(user_id)
