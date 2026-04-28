from datetime import datetime

import pytest
from pydantic import ValidationError

from schemas.watch_history import (
    WatchHistoryBase,
    WatchHistoryCreate,
    WatchHistoryResponse,
    WatchHistoryResponseList,
)
from tests.utils import (
    generate_random_number,
    create_watch_history_data,
    create_watch_history_response_list,
    create_watch_history_response_data,
)


@pytest.fixture(scope="function")
def watch_history_data() -> dict[str, int]:
    return create_watch_history_data()


@pytest.fixture(scope="function")
def watch_history_response_data() -> dict[str, str | int | datetime]:
    return create_watch_history_response_data()


@pytest.fixture(scope="function")
def watch_history_response_list() -> list[WatchHistoryResponse]:
    return create_watch_history_response_list(list_length=3)


@pytest.mark.parametrize(
    "schema",
    [
        WatchHistoryBase,
        WatchHistoryCreate,
    ],
)
class TestWatchHistoryBaseCreate:
    def test_watch_history(
        self,
        schema,
        watch_history_data: dict[str, int],
    ) -> None:
        watch_history = schema(**watch_history_data)
        assert watch_history.model_dump() == watch_history_data

    def test_watch_history_without_movie_id(
        self,
        schema,
        watch_history_data: dict[str, int],
    ) -> None:
        watch_history_data.pop("movie_id")
        with pytest.raises(
            ValidationError,
            match="Field required",
        ):
            schema(**watch_history_data)


class TestWatchHistoryResponse:
    def test_watch_history_without_id(
        self,
        watch_history_response_data: dict[str, str | int | datetime],
    ) -> None:
        watch_history_response_data.pop("id")
        with pytest.raises(ValidationError, match="Field required"):
            WatchHistoryResponse(**watch_history_response_data)

    def test_watch_history_without_user_id(
        self,
        watch_history_response_data: dict[str, str | int | datetime],
    ) -> None:
        watch_history_response_data.pop("user_id")
        with pytest.raises(ValidationError, match="Field required"):
            WatchHistoryResponse(**watch_history_response_data)

    def test_watch_history_without_watched_at_field(
        self,
        watch_history_response_data: dict[str, str | int | datetime],
    ) -> None:
        watch_history_response_data.pop("watched_at")
        with pytest.raises(ValidationError, match="Field required"):
            WatchHistoryResponse(**watch_history_response_data)


class TestWatchHistoryResponseList:
    def test_watch_history_response_list(
        self,
        watch_history_response_list: list[WatchHistoryResponse],
    ) -> None:
        page = generate_random_number()
        size = generate_random_number()
        schema = WatchHistoryResponseList(
            watch_history_list=watch_history_response_list,
            page=page,
            size=size,
        )
        assert schema.watch_history_list == watch_history_response_list
        assert schema.page == page
        assert schema.size == size

    def test_watch_history_response_list_with_empty_list(self) -> None:
        page = generate_random_number()
        size = generate_random_number()
        schema = WatchHistoryResponseList(
            watch_history_list=[],
            page=page,
            size=size,
        )
        assert len(schema.watch_history_list) == 0
        assert schema.page == page
        assert schema.size == size
