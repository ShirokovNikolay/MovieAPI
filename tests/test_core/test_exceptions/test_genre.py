import random

import pytest
from _pytest.fixtures import SubRequest

from core.constants import BASE_GENRE_ERROR
from core.exceptions.genre import (
    GenreNotFoundError,
    GenreAlreadyExistsError,
    GenreAlreadyHasMoviesError,
    GenreIdNotFoundError,
    GenreNameAlreadyExistsError,
    GenreIdAlreadyHasMoviesError,
)
from tests.test_core.test_exceptions.test_base import generate_list_of_random_strings


def generate_random_id() -> int:
    return random.randint(1, 1000)


def generate_random_id_list(list_length: int = 5) -> list[int]:
    return [generate_random_id() for _ in range(list_length)]


@pytest.fixture(
    scope="function",
    params=[
        GenreNotFoundError,
        GenreAlreadyExistsError,
        GenreAlreadyHasMoviesError,
    ],
)
def base_genre_error(request: SubRequest) -> BASE_GENRE_ERROR:
    return request.param


@pytest.fixture(
    scope="function",
    params=generate_random_id_list(list_length=5),
)
def genre_id(request: SubRequest) -> int:
    return request.param


@pytest.fixture(
    scope="function",
    params=generate_list_of_random_strings(list_length=5),
)
def genre_name(request: SubRequest) -> int:
    return request.param


def test_base_genre_error_can_raise_with_detail(
    base_genre_error: BASE_GENRE_ERROR,
    detail: str,
) -> None:
    with pytest.raises(
        base_genre_error,
        match=detail,
    ) as exc_info:
        raise base_genre_error(detail)
    assert exc_info.value.detail == detail


def test_genre_id_not_found_error_can_raise_with_detail(genre_id: int) -> None:
    with pytest.raises(
        GenreIdNotFoundError,
        match=str(genre_id),
    ) as exc_info:
        raise GenreIdNotFoundError(genre_id)
    assert exc_info.value.genre_id == genre_id


def test_genre_id_already_has_movies_error(genre_id: int) -> None:
    with pytest.raises(
        GenreIdAlreadyHasMoviesError,
        match=str(genre_id),
    ) as exc_info:
        raise GenreIdAlreadyHasMoviesError(genre_id)
    assert exc_info.value.genre_id == genre_id


def test_genre_id_already_exists_error_can_raise_with_detail(genre_name: str) -> None:
    with pytest.raises(
        GenreNameAlreadyExistsError,
        match=genre_name,
    ) as exc_info:
        raise GenreNameAlreadyExistsError(genre_name)
    assert exc_info.value.genre_name == genre_name
    assert genre_name in exc_info.value.detail
