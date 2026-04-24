import random
import string

import pytest
from _pytest.fixtures import SubRequest


def generate_random_id(start=1, end=1000) -> int:
    return random.randint(start, end)


def generate_random_id_list(
    list_length: int = 5,
    start=1,
    end=1000,
) -> list[int]:
    return [generate_random_id(start, end) for _ in range(list_length)]


def generate_random_string(
    min_string_length: int = 1,
    max_string_length: int = 10,
    string_length: int | None = None,
) -> str:
    if string_length is None:
        string_length = random.randint(min_string_length, max_string_length)

    return "".join(
        [
            random.choice(
                string.ascii_letters + string.digits,
            )
            for _ in range(string_length)
        ],
    )


def generate_list_of_random_strings(
    min_string_length: int = 1,
    max_string_length: int = 10,
    string_length: int | None = None,
    min_list_length: int = 1,
    max_list_length: int = 5,
    list_length: int | None = None,
) -> list[str]:
    if list_length is None:
        list_length = random.randint(min_list_length, max_list_length)

    return [
        generate_random_string(
            min_string_length,
            max_string_length,
            string_length,
        )
        for _ in range(list_length)
    ]


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
