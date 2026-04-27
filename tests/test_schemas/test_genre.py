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
from tests.utils import generate_random_number, generate_random_string

NAME_MIN_LENGTH = 3
NAME_MAX_LENGTH = 15
DESCRIPTION_MAX_LENGTH = 200


def create_genre_data():
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


def create_genre_response_data():
    data = create_genre_data()
    data["id"] = generate_random_number()
    return data


def create_genre_response_list(list_length: int = 5) -> list[GenreResponse]:
    genre_response_list = []
    for i in range(list_length):
        genre_data = create_genre_response_data()
        genre_response = GenreResponse(**genre_data)
        genre_response_list.append(genre_response)
    return genre_response_list


@pytest.fixture(scope="function")
def genre_data() -> dict[str, str]:
    return create_genre_data()


@pytest.fixture(scope="function")
def genre_response_data() -> dict[str, str | int]:
    return create_genre_response_data()


@pytest.fixture(scope="function")
def genre_response_list() -> list[GenreResponse]:
    return create_genre_response_list(list_length=3)


@pytest.mark.parametrize(
    "schema",
    [
        GenreBase,
        GenreCreate,
        GenreUpdate,
        GenreResponse,
    ],
)
class TestGenreBaseCreateUpdateResponse:
    def test_genre(
        self,
        schema,
        genre_response_data: dict[str, str | int],
    ) -> None:
        schema_object = schema(**genre_response_data)
        for field in schema_object.model_dump():
            assert getattr(schema_object, field) == genre_response_data[field]

    def test_genre_without_name(
        self,
        schema,
        genre_response_data: dict[str, str | int],
    ) -> None:
        genre_response_data.pop("name")
        with pytest.raises(ValidationError, match="Field required"):
            schema(**genre_response_data)

    def test_genre_without_description(
        self,
        schema,
        genre_response_data: dict[str, str | int],
    ) -> None:
        genre_response_data.pop("description")
        with pytest.raises(ValidationError, match="Field required"):
            schema(**genre_response_data)

    def test_genre_with_too_long_description_field(
        self,
        schema,
        genre_response_data: dict[str, str | int],
    ) -> None:
        genre_response_data["description"] = generate_random_string(
            string_length=DESCRIPTION_MAX_LENGTH + 1,
        )
        with pytest.raises(ValidationError, match="string_too_long"):
            schema(**genre_response_data)

    def test_genre_with_too_short_name_field(
        self,
        schema,
        genre_response_data: dict[str, str | int],
    ) -> None:
        genre_response_data["name"] = generate_random_string(
            string_length=NAME_MIN_LENGTH - 1
        )
        with pytest.raises(ValidationError, match="string_too_short"):
            schema(**genre_response_data)

    def test_genre_with_too_long_name_field(
        self,
        schema,
        genre_response_data: dict[str, str | int],
    ) -> None:
        genre_response_data["name"] = generate_random_string(
            string_length=NAME_MAX_LENGTH + 1
        )
        with pytest.raises(ValidationError, match="string_too_long"):
            schema(**genre_response_data)


class TestGenrePartialUpdate:
    def test_genre_partial_update(self, genre_data: dict[str, str]) -> None:
        schema = GenrePartialUpdate(**genre_data)
        assert schema.model_dump() == genre_data

    def test_genre_partial_update_without_name_field(
        self,
        genre_data: dict[str, str],
    ) -> None:
        genre_data.pop("name")
        schema = GenrePartialUpdate(**genre_data)
        assert schema.name is None
        assert schema.description == genre_data["description"]

    def test_genre_partial_update_without_description_field(
        self,
        genre_data: dict[str, str],
    ) -> None:
        genre_data.pop("description")
        schema = GenrePartialUpdate(**genre_data)
        assert schema.name == genre_data["name"]
        assert schema.description is None

    def test_genre_partial_update_with_too_short_name_field(
        self,
        genre_data: dict[str, str],
    ) -> None:
        genre_data["name"] = generate_random_string(string_length=NAME_MIN_LENGTH - 1)
        with pytest.raises(
            ValidationError,
            match="string_too_short",
        ):
            GenrePartialUpdate(**genre_data)

    def test_genre_partial_update_with_too_long_name_field(
        self,
        genre_data: dict[str, str],
    ) -> None:
        genre_data["name"] = generate_random_string(string_length=NAME_MAX_LENGTH + 1)
        with pytest.raises(
            ValidationError,
            match="string_too_long",
        ):
            GenrePartialUpdate(**genre_data)

    def test_genre_partial_update_with_too_long_description_field(
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
        page = generate_random_number()
        size = generate_random_number()
        schema = GenreResponseList(
            genre_list=genre_response_list,
            page=page,
            size=size,
        )
        assert schema.genre_list == genre_response_list
        assert schema.page == page
        assert schema.size == size

    def test_genre_response_list_with_empty_genre_list(self) -> None:
        page = generate_random_number()
        size = generate_random_number()
        schema = GenreResponseList(
            genre_list=[],
            page=page,
            size=size,
        )
        assert len(schema.genre_list) == 0
        assert schema.page == page
        assert schema.size == size
