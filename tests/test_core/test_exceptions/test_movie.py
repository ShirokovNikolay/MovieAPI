import pytest
from _pytest.fixtures import SubRequest

from core.constants import BASE_MOVIE_ERROR
from core.exceptions.movie import (
    MovieNotFoundError,
    MovieAlreadyExistsError,
    MovieIdNotFoundError,
    MovieNameAlreadyExistsError,
)


@pytest.fixture(
    scope="function",
    params=[
        MovieNotFoundError,
        MovieAlreadyExistsError,
    ],
)
def base_movie_error(request: SubRequest) -> BASE_MOVIE_ERROR:
    return request.param


def test_base_movie_error_raise_can_raise_with_detail(
    base_movie_error: BASE_MOVIE_ERROR,
    detail: str,
) -> None:
    with pytest.raises(
        base_movie_error,
        match=detail,
    ) as exc_info:
        raise base_movie_error(detail)
    assert exc_info.value.detail == detail


def test_movie_id_not_found_error_can_raise_with_detail(
    object_id: int,
) -> None:
    with pytest.raises(
        MovieIdNotFoundError,
        match=str(object_id),
    ) as exc_info:
        raise MovieIdNotFoundError(object_id)
    assert exc_info.value.movie_id == object_id
    assert str(object_id) in exc_info.value.detail


def test_movie_name_already_exists_error_can_raise_with_detail(
    name: str,
) -> None:
    with pytest.raises(
        MovieNameAlreadyExistsError,
        match=name,
    ) as exc_info:
        raise MovieNameAlreadyExistsError(name)
    assert exc_info.value.movie_name == name
    assert name in exc_info.value.detail
