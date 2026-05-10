from datetime import datetime

import pytest
from pydantic import ValidationError

from schemas.genre import (
    GenreCreate,
    GenrePartialUpdate,
    GenreResponse,
    GenreUpdate,
    GenreBase,
    GenreResponseList,
)
from core.constants import (
    GENRE_NAME_MIN_LENGTH,
    GENRE_NAME_MAX_LENGTH,
    GENRE_DESCRIPTION_MAX_LENGTH,
)
from tests.utils.data_generators.genre import (
    create_genre_data,
    create_genre_response_data,
    create_genre_response_list,
)
from tests.utils.data_generators.base import (
    generate_number,
    generate_string,
    check_schema_not_none_fields_is_valid,
)


@pytest.mark.parametrize(
    "schema",
    [
        GenreBase,
        GenreCreate,
        GenreUpdate,
        GenrePartialUpdate,
        GenreResponse,
    ],
)
class TestGenre:
    def test_genre(
        self,
        schema,
        genre_response_data: dict[str, str | int],
    ) -> None:
        schema_object = schema(**genre_response_data)
        for field in schema_object.model_dump():
            assert getattr(schema_object, field) == genre_response_data[field]

    @pytest.mark.parametrize(
        "field",
        [
            "name",
            "description",
        ],
    )
    def test_genre_without_field(
        self,
        schema,
        field: str,
        genre_response_data: dict[str, str | int],
    ) -> None:
        if schema is GenrePartialUpdate:
            pytest.skip(
                reason="GenrePartialUpdate schema does not have required fields"
            )

        genre_response_data.pop(field)
        with pytest.raises(ValidationError, match="Field required"):
            schema(**genre_response_data)

    @pytest.mark.parametrize(
        "field,value,expected_error_message",
        [
            (
                "name",
                generate_string(length=GENRE_NAME_MIN_LENGTH - 1),
                "string_too_short",
            ),
            (
                "name",
                generate_string(length=GENRE_NAME_MAX_LENGTH + 1),
                "string_too_long",
            ),
            (
                "description",
                generate_string(length=GENRE_DESCRIPTION_MAX_LENGTH + 1),
                "string_too_long",
            ),
        ],
    )
    def test_genre_with_not_valid_fields(
        self,
        schema,
        field: str,
        value: str,
        expected_error_message: str,
        genre_response_data: dict[str, str | int],
    ) -> None:
        genre_response_data[field] = value
        with pytest.raises(ValidationError, match=expected_error_message):
            schema(**genre_response_data)


class TestGenrePartialUpdate:
    def test_genre_partial_update_is_empty(self):
        genre_update_schema = GenrePartialUpdate()
        for field in genre_update_schema.model_dump():
            assert getattr(genre_update_schema, field) is None

    def test_genre_partial_update_without_field(
        self,
        genre_data: dict[str, str | datetime],
    ) -> None:
        genre_data_copy = genre_data.copy()
        for field in genre_data_copy:
            value = genre_data.pop(field)
            movie_update_schema = GenrePartialUpdate(**genre_data)
            check_schema_not_none_fields_is_valid(
                movie_update_schema,
                genre_data,
            )
            assert getattr(movie_update_schema, field) is None
            genre_data[field] = value


class TestGenreResponse:
    def test_genre_response_without_id_field(
        self,
        genre_response_data: dict[str, str | int],
    ) -> None:
        genre_response_data.pop("id")
        with pytest.raises(
            ValidationError,
            match="Field required",
        ):
            GenreResponse(**genre_response_data)


class TestGenreResponseList:
    def test_genre_response_list(
        self,
        genre_response_list: list[GenreResponse],
    ) -> None:
        page = generate_number()
        size = generate_number()
        schema = GenreResponseList(
            genre_list=genre_response_list,
            page=page,
            size=size,
        )
        assert schema.genre_list == genre_response_list
        assert schema.page == page
        assert schema.size == size

    def test_genre_response_list_with_empty_list(self) -> None:
        page = generate_number()
        size = generate_number()
        schema = GenreResponseList(
            genre_list=[],
            page=page,
            size=size,
        )
        assert len(schema.genre_list) == 0
        assert schema.page == page
        assert schema.size == size
