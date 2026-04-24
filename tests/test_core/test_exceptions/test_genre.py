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


def test_genre_name_already_exists_error_can_raise_with_detail(name: str) -> None:
    with pytest.raises(
        GenreNameAlreadyExistsError,
        match=name,
    ) as exc_info:
        raise GenreNameAlreadyExistsError(name)
    assert exc_info.value.genre_name == name
    assert name in exc_info.value.detail
