import pytest
from pydantic import ValidationError

from schemas.favorite_movie import (
    FavoriteMovieBase,
    FavoriteMovieCreate,
    FavoriteMovieResponse,
    FavoriteMovieResponseList,
)
from tests.utils import (
    generate_random_number,
    create_favorite_movie_response_data,
    create_favorite_movie_response_list_data,
)


@pytest.fixture(scope="function")
def favorite_movie_response_data() -> dict[str, int]:
    return create_favorite_movie_response_data()


@pytest.fixture(scope="function")
def favorite_movie_response_list() -> list[FavoriteMovieResponse]:
    return create_favorite_movie_response_list_data(list_length=3)


@pytest.mark.parametrize(
    "schema",
    [
        FavoriteMovieBase,
        FavoriteMovieCreate,
        FavoriteMovieResponse,
    ],
)
class TestFavoriteMovieBaseCreateResponse:
    def test_favorite_movie(
        self,
        favorite_movie_response_data: dict[str, int],
        schema,
    ) -> None:
        favorite_movie_schema = schema(**favorite_movie_response_data)
        for field in favorite_movie_schema.model_dump():
            assert (
                getattr(favorite_movie_schema, field)
                == favorite_movie_response_data[field]
            )

    def test_favorite_movie_without_movie_id(
        self,
        schema,
        favorite_movie_response_data: dict[str, int],
    ) -> None:
        favorite_movie_response_data.pop("movie_id")
        with pytest.raises(ValidationError, match="Field required"):
            schema(**favorite_movie_response_data)


class TestFavoriteMovieResponse:
    def test_favorite_movie_without_id(
        self,
        favorite_movie_response_data: dict[str, int],
    ) -> None:
        favorite_movie_response_data.pop("id")
        with pytest.raises(ValidationError, match="Field required"):
            FavoriteMovieResponse(**favorite_movie_response_data)


class TestFavoriteMovieResponseList:
    def test_favorite_movie_response_list(
        self,
        favorite_movie_response_list: list[FavoriteMovieResponse],
    ) -> None:
        page = generate_random_number()
        size = generate_random_number()
        schema = FavoriteMovieResponseList(
            favorite_movie_list=favorite_movie_response_list,
            page=page,
            size=size,
        )
        assert schema.favorite_movie_list == favorite_movie_response_list
        assert schema.page == page
        assert schema.size == size

    def test_favorite_movie_response_list_with_empty_list(self) -> None:
        page = generate_random_number()
        size = generate_random_number()
        schema = FavoriteMovieResponseList(
            favorite_movie_list=[],
            page=page,
            size=size,
        )
        assert len(schema.favorite_movie_list) == 0
        assert schema.page == page
        assert schema.size == size
