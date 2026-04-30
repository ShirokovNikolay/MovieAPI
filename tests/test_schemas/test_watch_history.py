from datetime import datetime

import pytest
from pydantic import ValidationError

from schemas.watch_history import (
    WatchHistoryBase,
    WatchHistoryCreate,
    WatchHistoryResponse,
    WatchHistoryResponseList,
)
from tests.utils.data_generators.watch_history import (
    create_watch_history_data,
    create_watch_history_response_list,
    create_watch_history_response_data,
)
from tests.utils.data_generators.base import generate_number


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
        WatchHistoryResponse,
    ],
)
class TestWatchHistory:
    def test_watch_history(
        self,
        schema,
        watch_history_response_data: dict[str, int | datetime],
    ) -> None:
        watch_history = schema(**watch_history_response_data)
        for field in watch_history.model_dump():
            assert getattr(watch_history, field) == watch_history_response_data[field]

    def test_watch_history_without_movie_id(
        self,
        schema,
        watch_history_response_data: dict[str, int],
    ) -> None:
        watch_history_response_data.pop("movie_id")
        with pytest.raises(
            ValidationError,
            match="Field required",
        ):
            schema(**watch_history_response_data)


class TestWatchHistoryResponseList:
    def test_watch_history_response_list(
        self,
        watch_history_response_list: list[WatchHistoryResponse],
    ) -> None:
        page = generate_number()
        size = generate_number()
        schema = WatchHistoryResponseList(
            watch_history_list=watch_history_response_list,
            page=page,
            size=size,
        )
        assert schema.watch_history_list == watch_history_response_list
        assert schema.page == page
        assert schema.size == size

    def test_watch_history_response_list_with_empty_list(self) -> None:
        page = generate_number()
        size = generate_number()
        schema = WatchHistoryResponseList(
            watch_history_list=[],
            page=page,
            size=size,
        )
        assert len(schema.watch_history_list) == 0
        assert schema.page == page
        assert schema.size == size
