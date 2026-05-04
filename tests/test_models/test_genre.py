import pytest
from sqlalchemy.exc import IntegrityError, DBAPIError
from sqlalchemy.ext.asyncio import AsyncSession

from core.constants import (
    GENRE_DESCRIPTION_MAX_LENGTH,
    GENRE_NAME_MIN_LENGTH,
    GENRE_NAME_MAX_LENGTH,
)
from models import Genre
from schemas.genre import GenreCreate
from tests.test_schemas.test_genre import genre_data
from tests.utils.data_generators.base import generate_string


@pytest.fixture(scope="function")
def genre_create_schema(genre_data: dict[str, str]) -> GenreCreate:
    return GenreCreate(**genre_data)


class TestGenreModel:
    async def test_create_genre(
        self,
        session: AsyncSession,
        genre_create_schema: GenreCreate,
    ) -> None:
        genre = Genre(**genre_create_schema.model_dump())
        session.add(genre)
        await session.flush()
        await session.refresh(genre)
        assert genre.id is not None
        assert genre.name == genre_create_schema.name
        assert genre.description == genre_create_schema.description
        assert genre.create_date is not None

    @pytest.mark.parametrize(
        "field,value,expected_error",
        [
            (
                "name",
                generate_string(length=GENRE_NAME_MIN_LENGTH - 1),
                IntegrityError,
            ),
            (
                "name",
                generate_string(length=GENRE_NAME_MAX_LENGTH + 1),
                DBAPIError,
            ),
            (
                "description",
                generate_string(length=GENRE_DESCRIPTION_MAX_LENGTH + 1),
                DBAPIError,
            ),
        ],
    )
    async def test_field_constraints_with_wrong_value(
        self,
        session: AsyncSession,
        field: str,
        value: str,
        expected_error,
        genre_data: dict[str, str],
    ) -> None:
        genre_data[field] = value
        genre = Genre(**genre_data)
        session.add(genre)
        with pytest.raises(expected_error):
            await session.flush()
