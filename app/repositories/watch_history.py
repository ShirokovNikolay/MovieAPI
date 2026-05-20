from datetime import date
from typing import cast as typing_cast

from sqlalchemy import Date, and_, cast, delete, desc, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from models import User, WatchHistory
from schemas.watch_history import WatchHistoryCreate


class WatchHistoryRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_watch_history_owner(self, watch_history_id: int) -> User | None:
        stmt = (
            select(User)
            .join(WatchHistory, User.id == WatchHistory.user_id)
            .where(WatchHistory.id == watch_history_id)
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_watch_history_by_id(
        self,
        watch_history_id: int,
    ) -> WatchHistory | None:
        stmt = (
            select(WatchHistory)
            .options(joinedload(WatchHistory.movie))
            .where(WatchHistory.id == watch_history_id)
        )
        result = await self.session.execute(stmt)
        return result.scalar()

    async def watch_history_exists(self, watch_history_id: int) -> bool:
        return await self.get_watch_history_by_id(watch_history_id) is not None

    async def get_watch_history_list(
        self,
        user_id: int,
        size: int = 10,
        page: int = 1,
    ) -> list[WatchHistory]:
        stmt = (
            select(WatchHistory)
            .options(joinedload(WatchHistory.movie))
            .where(WatchHistory.user_id == user_id)
            .order_by(desc(WatchHistory.watched_at))
            .limit(size)
            .offset(size * (page - 1))
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def get_watch_history_by_date_range(
        self,
        user_id: int,
        start_date: date,
        end_date: date,
        size: int = 10,
        page: int = 1,
    ) -> list[WatchHistory]:
        stmt = (
            select(WatchHistory)
            .options(joinedload(WatchHistory.movie))
            .where(
                and_(
                    WatchHistory.user_id == user_id,
                    start_date <= cast(WatchHistory.watched_at, Date),
                    cast(WatchHistory.watched_at, Date) <= end_date,
                ),
            )
            .order_by(desc(WatchHistory.watched_at))
            .limit(size)
            .offset(size * (page - 1))
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def count_user_watch_history(self, user_id: int) -> int:
        stmt = select(
            func.count(WatchHistory.id),
        ).where(
            WatchHistory.user_id == user_id,
        )
        result = await self.session.execute(stmt)
        return typing_cast(int, result.scalar())

    async def add_movie_to_watch_history(
        self,
        user_id: int,
        create_watch_history_data: WatchHistoryCreate,
    ) -> WatchHistory:
        movie_watch_history = WatchHistory(
            user_id=user_id,
            **create_watch_history_data.model_dump(),
        )
        self.session.add(movie_watch_history)
        await self.session.commit()
        await self.session.refresh(movie_watch_history)
        return movie_watch_history

    async def delete_watch_history_by_id(self, watch_history_id: int) -> bool:
        if not await self.watch_history_exists(watch_history_id):
            return False
        stmt = delete(WatchHistory).where(WatchHistory.id == watch_history_id)
        await self.session.execute(stmt)
        await self.session.commit()
        return True

    async def delete_user_watch_history(self, user_id: int) -> bool:
        if not await self.get_watch_history_list(user_id):
            return False

        stmt = delete(WatchHistory).where(WatchHistory.user_id == user_id)
        await self.session.execute(stmt)
        await self.session.commit()
        return True
