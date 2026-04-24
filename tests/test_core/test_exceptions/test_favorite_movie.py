import pytest
from _pytest.fixtures import SubRequest

from core.constants import BASE_MOVIE_ERROR, BASE_FAVORITE_MOVIE_ERROR
from core.exceptions.favorite_movie import (
    FavoriteMovieAlreadyExistsError,
    FavoriteMovieNotFoundError,
    FavoriteMovieNotFoundByUserAndMovieError,
    FavoriteMovieAlreadyExistsByUserAndMovieError,
    FavoriteMovieIdNotFoundError,
)


@pytest.fixture(
    scope="function",
    params=[
        FavoriteMovieNotFoundError,
        FavoriteMovieAlreadyExistsError,
    ],
)
def base_favorite_movie_error(request: SubRequest) -> BASE_MOVIE_ERROR:
    return request.param


def test_base_favorite_movie_error_can_raise_with_detail(
    base_favorite_movie_error: BASE_FAVORITE_MOVIE_ERROR,
    detail: str,
) -> None:
    with pytest.raises(
        base_favorite_movie_error,
        match=detail,
    ) as exc_info:
        raise base_favorite_movie_error(detail)
    assert exc_info.value.detail == detail


def test_favorite_movie_id_not_found_error_can_raise_with_detail(
    favorite_movie_id: int,
) -> None:
    with pytest.raises(
        FavoriteMovieIdNotFoundError,
        match=str(favorite_movie_id),
    ) as exc_info:
        raise FavoriteMovieIdNotFoundError(favorite_movie_id)
    assert exc_info.value.favorite_movie_id == favorite_movie_id
    assert str(favorite_movie_id) in exc_info.value.detail


def test_favorite_movie_not_found_by_user_and_movie_error_can_raise_with_detail(
    movie_id: int,
    user_id: int,
) -> None:
    with pytest.raises(
        FavoriteMovieNotFoundByUserAndMovieError,
    ) as exc_info:
        raise FavoriteMovieNotFoundByUserAndMovieError(user_id, movie_id)
    assert exc_info.value.movie_id == movie_id
    assert exc_info.value.user_id == user_id
    assert str(movie_id) in exc_info.value.detail
    assert str(user_id) in exc_info.value.detail


def test_favorite_movie_already_exists_by_user_and_movie_error_can_raise_with_detail(
    movie_id: int,
    user_id: int,
) -> None:
    with pytest.raises(
        FavoriteMovieAlreadyExistsByUserAndMovieError,
    ) as exc_info:
        raise FavoriteMovieAlreadyExistsByUserAndMovieError(user_id, movie_id)
    assert exc_info.value.movie_id == movie_id
    assert exc_info.value.user_id == user_id
    assert str(movie_id) in exc_info.value.detail
    assert str(user_id) in exc_info.value.detail
