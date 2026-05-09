from datetime import datetime

import pytest
from sqlalchemy.exc import IntegrityError, DBAPIError
from sqlalchemy.ext.asyncio import AsyncSession

from core.constants import (
    MOVIE_NAME_MAX_LENGTH,
    MOVIE_DESCRIPTION_MAX_LENGTH,
    MOVIE_RATING_MIN_VALUE,
)
from models import Genre, Movie
from tests.utils.data_generators.base import generate_string, generate_number


class TestMovieModel:
    async def test_create_movie(
        self,
        session: AsyncSession,
        movie_data: dict[str, str | int],
        genre_model: Genre,
    ) -> None:
        movie_data["genre_id"] = genre_model.id
        movie = Movie(**movie_data)
        session.add(movie)
        await session.flush()
        await session.refresh(movie)
        assert movie.name == movie_data["name"]
        assert movie.description == movie_data["description"]
        assert movie.rating == movie_data["rating"]
        assert movie.preview_url == movie_data["preview_url"]
        assert movie.source_url == movie_data["source_url"]
        assert movie.genre_id == genre_model.id
        assert movie.release_date == movie_data["release_date"]

    @pytest.mark.parametrize(
        "field,value,expected_error",
        [
            (
                "name",
                generate_string(length=MOVIE_NAME_MAX_LENGTH - 1),
                IntegrityError,
            ),
            (
                "name",
                generate_string(length=MOVIE_NAME_MAX_LENGTH + 1),
                DBAPIError,
            ),
            (
                "description",
                generate_string(length=MOVIE_DESCRIPTION_MAX_LENGTH + 1),
                DBAPIError,
            ),
            (
                "rating",
                generate_string(length=MOVIE_RATING_MIN_VALUE - 1),
                DBAPIError,
            ),
            (
                "rating",
                generate_string(length=MOVIE_RATING_MIN_VALUE + 1),
                DBAPIError,
            ),
            (
                "source_url",
                generate_string(length=0),
                IntegrityError,
            ),
            (
                "preview_url",
                generate_string(length=0),
                IntegrityError,
            ),
            (
                "genre_id",
                generate_number(start=-100, end=0),
                IntegrityError,
            ),
        ],
    )
    async def test_movie_with_wrong_values(
        self,
        session: AsyncSession,
        movie_data: dict[str | int | datetime],
        field: str,
        value: str,
        expected_error,
    ) -> None:
        movie_data[field] = value
        movie = Movie(**movie_data)
        session.add(movie)
        with pytest.raises(expected_error):
            await session.flush()
