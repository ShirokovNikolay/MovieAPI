import pytest
from core.exceptions.watch_history import (
    WatchHistoryNotFoundError,
    WatchHistoryIdNotFoundError,
)


def test_watch_history_not_found_error_can_raise_with_detail(detail: str) -> None:
    with pytest.raises(
        WatchHistoryNotFoundError,
        match=detail,
    ) as exc_info:
        raise WatchHistoryNotFoundError(detail)
    assert exc_info.value.detail == detail


def test_watch_history_id_not_found_error_can_raise_with_detail(
    watch_history_id: int,
) -> None:
    with pytest.raises(
        WatchHistoryIdNotFoundError,
        match=str(watch_history_id),
    ) as exc_info:
        raise WatchHistoryIdNotFoundError(watch_history_id)
    assert exc_info.value.watch_history_id == watch_history_id
