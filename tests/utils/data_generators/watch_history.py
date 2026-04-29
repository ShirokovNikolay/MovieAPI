from datetime import datetime

from schemas.watch_history import WatchHistoryResponse
from tests.utils.data_generators.base import generate_number


def create_watch_history_data() -> dict[str, int]:
    data = {
        "movie_id": generate_number(1, 1000),
    }
    return data


def create_watch_history_response_data() -> dict[str, str | int | datetime]:
    data = create_watch_history_data()
    data["id"] = generate_number()
    data["user_id"] = generate_number()
    data["watched_at"] = datetime(
        year=generate_number(2020, 2025),
        month=generate_number(1, 12),
        day=generate_number(1, 28),
    )
    return data


def create_watch_history_response_list(
    list_length: int = 5,
) -> list[WatchHistoryResponse]:
    result = []
    for i in range(list_length):
        watch_history_data = create_watch_history_response_data()
        watch_history_response = WatchHistoryResponse(**watch_history_data)
        result.append(watch_history_response)
    return result
