import pytest
from sqlalchemy.exc import DBAPIError
from sqlalchemy.ext.asyncio import AsyncSession

from models import Movie, User, WatchHistory
from tests.utils.data_generators.base import generate_number


class TestWatchHistoryModel:
    async def test_watch_history(
        self,
        session: AsyncSession,
        movie: Movie,
        user: User,
        watch_history_response_data: dict,
    ) -> None:
        watch_history_response_data["movie_id"] = movie.id
        watch_history_response_data["user_id"] = user.id
        watch_history = WatchHistory(**watch_history_response_data)
        session.add(watch_history)
        await session.flush()
        await session.refresh(watch_history)
        assert watch_history.movie_id == watch_history_response_data["movie_id"]
        assert watch_history.user_id == watch_history_response_data["user_id"]
        assert watch_history.watched_at == watch_history_response_data["watched_at"]

    @pytest.mark.parametrize(
        "field,value,expected_error",
        [
            ("user_id", generate_number(-100, -1), DBAPIError),
            ("movie_id", generate_number(-100, -1), DBAPIError),
        ],
    )
    async def test_watch_history_with_wrong_values(
        self,
        field: str,
        value: int,
        expected_error,
        watch_history: WatchHistory,
        session: AsyncSession,
    ) -> None:
        setattr(watch_history, field, value)
        with pytest.raises(expected_error):
            await session.flush()
