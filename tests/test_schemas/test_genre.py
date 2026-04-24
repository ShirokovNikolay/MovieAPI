import pytest
from pydantic import ValidationError

from schemas.genre import GenreCreate, GenrePartialUpdate, GenreResponse, GenreUpdate
from tests.utils import generate_random_id, generate_random_string


@pytest.fixture(scope="function")
def genre_data() -> dict[str, str]:
    data = {
        "name": generate_random_string(
            min_string_length=3,
            max_string_length=15,
        ),
        "description": generate_random_string(
            min_string_length=0,
            max_string_length=200,
        ),
    }
    return data


@pytest.fixture(scope="function")
def genre_response_data(genre_data: dict[str, str]) -> dict[str, str | int]:
    genre_data["id"] = generate_random_id(start=1, end=100)
    return genre_data


NAME_MIN_LENGTH = 3
NAME_MAX_LENGTH = 15
DESCRIPTION_MAX_LENGTH = 200


class TestGenreCreateSchema:

    def test_genre_create_schema(self, genre_data) -> None:
        schema = GenreCreate(**genre_data)
        assert schema.model_dump() == genre_data

    def test_genre_create_schema_without_name_field(self, genre_data) -> None:
        genre_data.pop("name")
        with pytest.raises(ValidationError, match="Field required"):
            GenreCreate(**genre_data)

    def test_genre_create_schema_with_too_long_description_field(
        self,
        genre_data,
    ) -> None:
        genre_data["description"] = generate_random_string(
            string_length=DESCRIPTION_MAX_LENGTH + 1,
        )
        with pytest.raises(ValidationError, match="string_too_long"):
            GenreCreate(**genre_data)

    def test_genre_create_schema_with_too_short_name_field(self, genre_data) -> None:
        genre_data["name"] = generate_random_string(string_length=NAME_MIN_LENGTH - 1)
        with pytest.raises(ValidationError, match="string_too_short"):
            GenreCreate(**genre_data)

    def test_genre_create_schema_with_too_long_name_field(self, genre_data) -> None:
        genre_data["name"] = generate_random_string(string_length=NAME_MAX_LENGTH + 1)
        with pytest.raises(ValidationError, match="string_too_long"):
            GenreCreate(**genre_data)


class TestGenreUpdateSchema:
    def test_genre_update_schema(self, genre_data: dict[str, str]) -> None:
        schema = GenreUpdate(**genre_data)
        assert schema.name == genre_data["name"]
        assert schema.description == genre_data["description"]

    def test_genre_update_schema_without_name_field(
        self,
        genre_data: dict[str, str],
    ) -> None:
        genre_data.pop("name")
        with pytest.raises(
            ValidationError,
            match="Field required",
        ):
            GenreUpdate(**genre_data)

    def test_genre_update_schema_without_description_field(
        self,
        genre_data: dict[str, str],
    ) -> None:
        genre_data.pop("description")
        with pytest.raises(
            ValidationError,
            match="Field required",
        ):
            GenreUpdate(**genre_data)

    def test_genre_update_schema_with_too_short_name_field(
        self,
        genre_data: dict[str, str],
    ) -> None:
        genre_data["name"] = generate_random_string(string_length=NAME_MIN_LENGTH - 1)
        with pytest.raises(
            ValidationError,
            match="string_too_short",
        ):
            GenreUpdate(**genre_data)

    def test_genre_update_schema_with_too_long_name_field(
        self,
        genre_data: dict[str, str],
    ) -> None:
        genre_data["name"] = generate_random_string(string_length=NAME_MAX_LENGTH + 1)
        with pytest.raises(
            ValidationError,
            match="string_too_long",
        ):
            GenreUpdate(**genre_data)

    def test_genre_update_schema_with_too_long_description_field(
        self,
        genre_data: dict[str, str],
    ) -> None:
        genre_data["description"] = generate_random_string(
            string_length=DESCRIPTION_MAX_LENGTH + 1,
        )
        with pytest.raises(
            ValidationError,
            match="string_too_long",
        ):
            GenreUpdate(**genre_data)


class TestGenrePartialUpdateSchema:
    def test_genre_partial_update_schema(self, genre_data: dict[str, str]) -> None:
        schema = GenrePartialUpdate(**genre_data)
        assert schema.model_dump() == genre_data

    def test_genre_partial_update_schema_without_name_field(
        self,
        genre_data: dict[str, str],
    ) -> None:
        genre_data.pop("name")
        schema = GenrePartialUpdate(**genre_data)
        assert schema.name is None
        assert schema.description == genre_data["description"]

    def test_genre_partial_update_schema_without_description_field(
        self,
        genre_data: dict[str, str],
    ) -> None:
        genre_data.pop("description")
        schema = GenrePartialUpdate(**genre_data)
        assert schema.name == genre_data["name"]
        assert schema.description is None

    def test_genre_partial_update_schema_with_too_short_name_field(
        self,
        genre_data: dict[str, str],
    ) -> None:
        genre_data["name"] = generate_random_string(string_length=NAME_MIN_LENGTH - 1)
        with pytest.raises(
            ValidationError,
            match="string_too_short",
        ):
            GenrePartialUpdate(**genre_data)

    def test_genre_partial_update_schema_with_too_long_name_field(
        self,
        genre_data: dict[str, str],
    ) -> None:
        genre_data["name"] = generate_random_string(string_length=NAME_MAX_LENGTH + 1)
        with pytest.raises(
            ValidationError,
            match="string_too_long",
        ):
            GenrePartialUpdate(**genre_data)

    def test_genre_partial_update_schema_with_too_long_description_field(
        self,
        genre_data: dict[str, str],
    ) -> None:
        genre_data["description"] = generate_random_string(
            string_length=DESCRIPTION_MAX_LENGTH + 1,
        )
        with pytest.raises(
            ValidationError,
            match="string_too_long",
        ):
            GenrePartialUpdate(**genre_data)
