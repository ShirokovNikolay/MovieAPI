import pytest
from sqlalchemy.exc import IntegrityError, DBAPIError
from sqlalchemy.ext.asyncio import AsyncSession

from core.constants import (
    GENRE_DESCRIPTION_MAX_LENGTH,
    GENRE_NAME_MIN_LENGTH,
    GENRE_NAME_MAX_LENGTH,
)
from models import Genre
from tests.utils.data_generators.base import generate_string


class TestGenreModel:
    async def test_create_genre(
        self,
        session: AsyncSession,
        genre_data: dict[str, str],
    ) -> None:
        genre = Genre(**genre_data)
        session.add(genre)
        await session.flush()
        await session.refresh(genre)
        assert genre.id is not None
        assert genre.name == genre_data["name"]
        assert genre.description == genre_data["description"]
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

    async def test_genre_name_unique_constraint(
        self,
        session: AsyncSession,
        genre_data: dict[str, str],
        genre: Genre,
    ) -> None:
        genre_data["name"] = genre.name
        genre_candidate = Genre(**genre_data)
        session.add(genre_candidate)
        with pytest.raises(IntegrityError):
            await session.flush()
