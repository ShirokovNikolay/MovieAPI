from datetime import datetime

import pytest
from pydantic import ValidationError

from schemas.movie import (
    MovieBase,
    MovieCreate,
    MovieUpdate,
    MovieResponse,
    MoviePartialUpdate,
    MovieResponseList,
)
from tests.utils import generate_random_number, generate_random_string
from faker import Faker

NAME_MIN_LENGTH = 3
NAME_MAX_LENGTH = 20
DESCRIPTION_MIN_LENGTH = 0
DESCRIPTION_MAX_LENGTH = 200
RATING_MIN_VALUE = 0
RATING_MAX_VALUE = 10


def create_movie_data() -> dict[str, str | datetime]:
    faker = Faker()
    data = {
        "name": generate_random_string(
            min_string_length=NAME_MIN_LENGTH,
            max_string_length=NAME_MAX_LENGTH,
        ),
        "description": generate_random_string(
            min_string_length=DESCRIPTION_MIN_LENGTH,
            max_string_length=DESCRIPTION_MAX_LENGTH,
        ),
        "rating": generate_random_number(RATING_MIN_VALUE, RATING_MAX_VALUE) / 10,
        "preview_url": faker.url(),
        "source_url": faker.url(),
        "genre_id": generate_random_number(0, 100),
        "release_date": datetime(
            year=generate_random_number(2020, 2025),
            month=generate_random_number(1, 12),
            day=generate_random_number(1, 28),
        ),
    }
    return data


def create_movie_response_data() -> dict[str, str | int | datetime]:
    data = create_movie_data()
    data["id"] = generate_random_number()
    return data


def create_movie_response_list(list_length: int = 5) -> list[MovieResponse]:
    result = []
    for i in range(list_length):
        movie_data = create_movie_response_data()
        movie_response_schema = MovieResponse(**movie_data)
        result.append(movie_response_schema)
    return result


def check_schema_not_none_fields_is_valid(schema, data) -> None:
    for field in schema.model_dump(exclude_none=True):
        assert getattr(schema, field) == data[field]


@pytest.fixture(scope="function")
def movie_data():
    return create_movie_data()


@pytest.fixture(scope="function")
def movie_response_data():
    return create_movie_response_data()


@pytest.fixture(scope="function")
def movie_response_list():
    return create_movie_response_list(list_length=3)


@pytest.mark.parametrize(
    "schema",
    [
        MovieBase,
        MovieCreate,
        MovieUpdate,
        MovieResponse,
    ],
)
class TestMovieBaseCreateUpdateResponse:
    def test_movie(
        self,
        schema,
        movie_response_data: dict[str, str | int],
    ) -> None:
        movie_schema = schema(**movie_response_data)
        for field in movie_schema.model_dump():
            assert getattr(movie_schema, field) == movie_response_data[field]

    def test_movie_without_name_field(
        self,
        schema,
        movie_response_data: dict[str, str | int],
    ) -> None:
        movie_response_data.pop("name")
        with pytest.raises(
            ValidationError,
            match="Field required",
        ):
            schema(**movie_response_data)

    def test_movie_without_description_field(
        self,
        schema,
        movie_response_data: dict[str, str | int],
    ) -> None:
        movie_response_data.pop("description")
        with pytest.raises(
            ValidationError,
            match="Field required",
        ):
            schema(**movie_response_data)

    def test_movie_without_rating_field(
        self,
        schema,
        movie_response_data: dict[str, str | int],
    ) -> None:
        movie_response_data.pop("rating")
        with pytest.raises(
            ValidationError,
            match="Field required",
        ):
            schema(**movie_response_data)

    def test_movie_without_preview_url_field(
        self,
        schema,
        movie_response_data: dict[str, str | int],
    ) -> None:
        movie_response_data.pop("preview_url")
        with pytest.raises(
            ValidationError,
            match="Field required",
        ):
            schema(**movie_response_data)

    def test_movie_without_source_url_field(
        self,
        schema,
        movie_response_data: dict[str, str | int],
    ) -> None:
        movie_response_data.pop("source_url")
        with pytest.raises(
            ValidationError,
            match="Field required",
        ):
            schema(**movie_response_data)

    def test_movie_without_genre_id_field(
        self,
        schema,
        movie_response_data: dict[str, str | int],
    ) -> None:
        movie_response_data.pop("genre_id")
        with pytest.raises(
            ValidationError,
            match="Field required",
        ):
            schema(**movie_response_data)

    def test_movie_without_release_date_field(
        self,
        schema,
        movie_response_data: dict[str, str | int],
    ) -> None:
        movie_response_data.pop("release_date")
        with pytest.raises(
            ValidationError,
            match="Field required",
        ):
            schema(**movie_response_data)

    def test_movie_with_too_short_name_field(
        self,
        schema,
        movie_response_data: dict[str, str | int],
    ) -> None:
        movie_response_data["name"] = generate_random_string(
            string_length=NAME_MIN_LENGTH - 1
        )
        with pytest.raises(ValidationError, match="string_too_short"):
            schema(**movie_response_data)

    def test_movie_with_too_long_name_field(
        self,
        schema,
        movie_response_data: dict[str, str | int],
    ) -> None:
        movie_response_data["name"] = generate_random_string(
            string_length=NAME_MAX_LENGTH + 1
        )
        with pytest.raises(ValidationError, match="string_too_long"):
            schema(**movie_response_data)

    def test_movie_with_too_long_description_field(
        self,
        schema,
        movie_response_data: dict[str, str | int],
    ) -> None:
        movie_response_data["description"] = generate_random_string(
            string_length=DESCRIPTION_MAX_LENGTH + 1
        )
        with pytest.raises(ValidationError, match="string_too_long"):
            schema(**movie_response_data)

    def test_movie_with_too_small_rating_field(
        self,
        schema,
        movie_response_data: dict[str, str | int],
    ) -> None:
        movie_response_data["rating"] = RATING_MIN_VALUE - 1
        with pytest.raises(ValidationError):
            schema(**movie_response_data)

    def test_movie_with_too_large_rating_field(
        self,
        schema,
        movie_response_data: dict[str, str | int],
    ) -> None:
        movie_response_data["rating"] = RATING_MAX_VALUE + 1
        with pytest.raises(ValidationError):
            schema(**movie_response_data)


class TestMoviePartialUpdate:
    def test_movie_partial_update(
        self,
        movie_data: dict[str, str | datetime],
    ) -> None:
        movie_update_schema = MoviePartialUpdate(**movie_data)
        assert movie_update_schema.model_dump() == movie_data

    def test_movie_partial_update_is_empty(self):
        movie_update_schema = MoviePartialUpdate()
        for field in movie_update_schema.model_dump():
            assert getattr(movie_update_schema, field) is None

    def test_movie_partial_update_without_any_field(
        self,
        movie_data: dict[str, str | datetime],
    ) -> None:
        movie_data_copy = movie_data.copy()
        for field in movie_data_copy:
            value = movie_data.pop(field)
            movie_update_schema = MoviePartialUpdate(**movie_data)
            check_schema_not_none_fields_is_valid(
                movie_update_schema,
                movie_data,
            )
            assert getattr(movie_update_schema, field) is None
            movie_data[field] = value

    def test_movie_partial_update_with_too_short_name_field(
        self,
        movie_data: dict[str, str | int | datetime],
    ) -> None:
        movie_data["name"] = generate_random_string(string_length=NAME_MIN_LENGTH - 1)
        with pytest.raises(ValidationError, match="string_too_short"):
            MoviePartialUpdate(**movie_data)

    def test_movie_partial_update_with_too_long_name_field(
        self,
        movie_data: dict[str, str | int | datetime],
    ) -> None:
        movie_data["name"] = generate_random_string(string_length=NAME_MAX_LENGTH + 1)
        with pytest.raises(ValidationError, match="string_too_long"):
            MoviePartialUpdate(**movie_data)

    def test_movie_partial_update_schema_too_long_description_field(
        self,
        movie_data: dict[str, str | int | datetime],
    ) -> None:
        movie_data["description"] = generate_random_string(
            string_length=DESCRIPTION_MAX_LENGTH + 1
        )
        with pytest.raises(ValidationError, match="string_too_long"):
            MoviePartialUpdate(**movie_data)

    def test_movie_partial_update_with_too_small_rating_field(
        self,
        movie_data: dict[str, str | int | datetime],
    ) -> None:
        movie_data["rating"] = RATING_MIN_VALUE - 1
        with pytest.raises(ValidationError, match="greater_than_equal"):
            MoviePartialUpdate(**movie_data)

    def test_movie_partial_update_with_too_large_rating_field(
        self,
        movie_data: dict[str, str | int | datetime],
    ) -> None:
        movie_data["rating"] = RATING_MAX_VALUE + 1
        with pytest.raises(ValidationError, match="less_than_equal"):
            MoviePartialUpdate(**movie_data)


class TestMovieResponseList:
    def test_movie_response_list(
        self,
        movie_response_list: list[MovieResponse],
    ) -> None:
        page = generate_random_number()
        size = generate_random_number()
        schema = MovieResponseList(
            movie_list=movie_response_list,
            page=page,
            size=size,
        )
        assert schema.movie_list == movie_response_list
        assert schema.page == page
        assert schema.size == size

    def test_genre_response_list_with_empty_list(self) -> None:
        page = generate_random_number()
        size = generate_random_number()
        schema = MovieResponseList(
            movie_list=[],
            page=page,
            size=size,
        )
        assert len(schema.movie_list) == 0
        assert schema.page == page
        assert schema.size == size
