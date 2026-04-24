import pytest
from _pytest.fixtures import SubRequest

from tests.utils import generate_list_of_random_strings, generate_random_id_list


@pytest.fixture(
    scope="function",
    params=generate_list_of_random_strings(
        list_length=3,
    ),
)
def detail(request: SubRequest) -> str:
    return request.param


@pytest.fixture(
    scope="function",
    params=generate_list_of_random_strings(
        list_length=3,
    ),
)
def name(request: SubRequest) -> str:
    return request.param


@pytest.fixture(
    scope="function",
    params=generate_random_id_list(
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
