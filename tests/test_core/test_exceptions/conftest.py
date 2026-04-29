import pytest
from _pytest.fixtures import SubRequest

from tests.utils.data_generators.base import generate_strings, generate_numbers


@pytest.fixture(
    scope="function",
    params=generate_strings(
        list_length=3,
    ),
)
def detail(request: SubRequest) -> str:
    return request.param


@pytest.fixture(
    scope="function",
    params=generate_strings(
        list_length=3,
    ),
)
def name(request: SubRequest) -> str:
    return request.param


@pytest.fixture(
    scope="function",
    params=generate_numbers(
        list_length=3,
    ),
)
def object_id(request: SubRequest) -> int:
    return request.param


@pytest.fixture(scope="function")
def genre_id(object_id: int) -> int:
    return object_id


@pytest.fixture(scope="function")
def movie_id(object_id: int) -> int:
    return object_id


@pytest.fixture(scope="function")
def favorite_movie_id(object_id: int) -> int:
    return object_id


@pytest.fixture(scope="function")
def user_id(object_id: int) -> int:
    return object_id


@pytest.fixture(scope="function")
def review_id(object_id: int) -> int:
    return object_id


@pytest.fixture(scope="function")
def watch_history_id(object_id: int) -> int:
    return object_id
