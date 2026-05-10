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
from core.constants import (
    MOVIE_NAME_MIN_LENGTH,
    MOVIE_NAME_MAX_LENGTH,
    MOVIE_DESCRIPTION_MAX_LENGTH,
    MOVIE_RATING_MIN_VALUE,
    MOVIE_RATING_MAX_VALUE,
)
from tests.utils.data_generators.base import (
    generate_number,
    generate_string,
    check_schema_not_none_fields_is_valid,
)


@pytest.mark.parametrize(
    "schema",
    [
        MovieBase,
        MovieCreate,
        MovieUpdate,
        MoviePartialUpdate,
        MovieResponse,
    ],
)
class TestMovie:
    def test_movie(
        self,
        schema,
        movie_response_data: dict[str, str | int],
    ) -> None:
        movie_schema = schema(**movie_response_data)
        for field in movie_schema.model_dump():
            assert getattr(movie_schema, field) == movie_response_data[field]

    @pytest.mark.parametrize(
        "field",
        [
            "name",
            "description",
            "rating",
            "preview_url",
            "source_url",
            "genre_id",
            "release_date",
        ],
    )
    def test_movie_without_field(
        self,
        schema,
        field: str,
        movie_response_data: dict[str, str | int],
    ) -> None:
        if schema is MoviePartialUpdate:
            pytest.skip(
                reason="Movie partial update schema does not have required fields"
            )
        movie_response_data.pop(field)
        with pytest.raises(ValidationError, match="Field required"):
            schema(**movie_response_data)

    @pytest.mark.parametrize(
        "field,value,expected_error_message",
        [
            (
                "name",
                generate_string(length=MOVIE_NAME_MIN_LENGTH - 1),
                "string_too_short",
            ),
            (
                "name",
                generate_string(length=MOVIE_NAME_MAX_LENGTH + 1),
                "string_too_long",
            ),
            (
                "description",
                generate_string(length=MOVIE_DESCRIPTION_MAX_LENGTH + 1),
                "string_too_long",
            ),
        ],
    )
    def test_movie_with_not_valid_field_length(
        self,
        schema,
        field: str,
        value: str,
        expected_error_message: str,
        movie_response_data: dict[str, str | int],
    ) -> None:
        movie_response_data[field] = value
        with pytest.raises(ValidationError, match=expected_error_message):
            schema(**movie_response_data)

    @pytest.mark.parametrize(
        "field,value,expected_error_message",
        [
            (
                "rating",
                MOVIE_RATING_MIN_VALUE - 1,
                "greater_than_equal",
            ),
            (
                "rating",
                MOVIE_RATING_MAX_VALUE + 1,
                "less_than_equal",
            ),
        ],
    )
    def test_movie_with_not_valid_value(
        self,
        schema,
        field: str,
        value: int,
        expected_error_message: str,
        movie_response_data: dict[str, str | int],
    ) -> None:
        movie_response_data[field] = value
        with pytest.raises(ValidationError, match=expected_error_message):
            schema(**movie_response_data)


class TestMoviePartialUpdate:
    def test_movie_partial_update_is_empty(self):
        movie_update_schema = MoviePartialUpdate()
        for field in movie_update_schema.model_dump():
            assert getattr(movie_update_schema, field) is None

    def test_movie_partial_update_without_field(
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


class TestMovieResponseList:
    def test_movie_response_list(
        self,
        movie_response_list: list[MovieResponse],
    ) -> None:
        page = generate_number()
        size = generate_number()
        schema = MovieResponseList(
            movie_list=movie_response_list,
            page=page,
            size=size,
        )
        assert schema.movie_list == movie_response_list
        assert schema.page == page
        assert schema.size == size

    def test_movie_response_list_with_empty_list(self) -> None:
        page = generate_number()
        size = generate_number()
        schema = MovieResponseList(
            movie_list=[],
            page=page,
            size=size,
        )
        assert len(schema.movie_list) == 0
        assert schema.page == page
        assert schema.size == size
