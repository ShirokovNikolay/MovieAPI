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
)


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
        genre_response_data["description"] = generate_string(
            length=GENRE_DESCRIPTION_MAX_LENGTH + 1,
        )
        with pytest.raises(ValidationError, match="string_too_long"):
            schema(**genre_response_data)

    def test_genre_with_too_short_name_field(
        self,
        schema,
        genre_response_data: dict[str, str | int],
    ) -> None:
        genre_response_data["name"] = generate_string(length=GENRE_NAME_MIN_LENGTH - 1)
        with pytest.raises(ValidationError, match="string_too_short"):
            schema(**genre_response_data)

    def test_genre_with_too_long_name_field(
        self,
        schema,
        genre_response_data: dict[str, str | int],
    ) -> None:
        genre_response_data["name"] = generate_string(length=GENRE_NAME_MAX_LENGTH + 1)
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
        genre_data["name"] = generate_string(length=GENRE_NAME_MIN_LENGTH - 1)
        with pytest.raises(
            ValidationError,
            match="string_too_short",
        ):
            GenrePartialUpdate(**genre_data)

    def test_genre_partial_update_with_too_long_name_field(
        self,
        genre_data: dict[str, str],
    ) -> None:
        genre_data["name"] = generate_string(length=GENRE_NAME_MAX_LENGTH + 1)
        with pytest.raises(
            ValidationError,
            match="string_too_long",
        ):
            GenrePartialUpdate(**genre_data)

    def test_genre_partial_update_with_too_long_description_field(
        self,
        genre_data: dict[str, str],
    ) -> None:
        genre_data["description"] = generate_string(
            length=GENRE_DESCRIPTION_MAX_LENGTH + 1,
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
