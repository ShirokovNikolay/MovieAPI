import pytest
from _pytest.fixtures import SubRequest

from core.constants import BASE_REVIEW_ERROR
from core.exceptions.review import (
    ReviewNotFoundError,
    ReviewAlreadyExistsError,
    ReviewIdNotFoundError,
    ReviewNotFoundByUserAndMovieError,
    ReviewAlreadyExistsByUserAndMovieError,
)


@pytest.fixture(
    scope="function",
    params=[
        ReviewNotFoundError,
        ReviewAlreadyExistsError,
    ],
)
def base_review_error(request: SubRequest) -> BASE_REVIEW_ERROR:
    return request.param


def test_base_review_error_can_raise_with_detail(
    base_review_error: BASE_REVIEW_ERROR,
    detail: str,
) -> None:
    with pytest.raises(
        base_review_error,
        match=detail,
    ) as exc_info:
        raise base_review_error(detail)
    assert exc_info.value.detail == detail


def test_review_id_not_found_error_can_raise_with_detail(review_id: int) -> None:
    with pytest.raises(ReviewIdNotFoundError, match=str(review_id)) as exc_info:
        raise ReviewIdNotFoundError(review_id)
    assert exc_info.value.review_id == review_id


def test_review_not_found_by_user_and_movie_error_can_raise_with_detail(
    user_id: int, movie_id: int
) -> None:
    with pytest.raises(
        ReviewNotFoundByUserAndMovieError, match=str(movie_id)
    ) as exc_info:
        raise ReviewNotFoundByUserAndMovieError(user_id, movie_id)
    assert exc_info.value.user_id == user_id
    assert exc_info.value.movie_id == movie_id


def test_review_already_exists_by_user_and_movie_error_can_raise_with_detail(
    user_id: int, movie_id: int
) -> None:
    with pytest.raises(
        ReviewAlreadyExistsByUserAndMovieError, match=str(movie_id)
    ) as exc_info:
        raise ReviewAlreadyExistsByUserAndMovieError(user_id, movie_id)
    assert exc_info.value.user_id == user_id
    assert exc_info.value.movie_id == movie_id
