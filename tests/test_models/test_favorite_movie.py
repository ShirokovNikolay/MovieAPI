import pytest
from sqlalchemy.exc import DBAPIError, IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from models import Movie, User, FavoriteMovie
from tests.utils.data_generators.base import generate_number


class TestFavoriteMovieModel:
    async def test_create_favorite_movie(
        self,
        session: AsyncSession,
        movie: Movie,
        user: User,
        favorite_movie_response_data: dict,
    ) -> None:
        favorite_movie_response_data["movie_id"] = movie.id
        favorite_movie_response_data["user_id"] = user.id
        favorite_movie = FavoriteMovie(**favorite_movie_response_data)
        session.add(favorite_movie)
        await session.flush()
        await session.refresh(favorite_movie)
        assert favorite_movie.id is not None
        assert favorite_movie.movie_id == favorite_movie_response_data["movie_id"]
        assert favorite_movie.user_id == favorite_movie_response_data["user_id"]

    @pytest.mark.parametrize(
        "field,value,expected_error",
        [
            ("movie_id", generate_number(start=-100, end=-1), DBAPIError),
            ("user_id", generate_number(start=-100, end=-1), DBAPIError),
        ],
    )
    async def test_favorite_movie_with_wrong_values(
        self,
        field: str,
        value: int,
        session: AsyncSession,
        favorite_movie: FavoriteMovie,
        expected_error,
    ) -> None:
        setattr(favorite_movie, field, value)
        with pytest.raises(expected_error):
            await session.flush()

    async def test_favorite_movie_unique_constraint(
        self,
        session: AsyncSession,
        favorite_movie_response_data: dict[str, int],
        favorite_movie: FavoriteMovie,
    ) -> None:
        favorite_movie_response_data["movie_id"] = favorite_movie.movie_id
        favorite_movie_response_data["user_id"] = favorite_movie.user_id
        favorite_movie_candidate = FavoriteMovie(**favorite_movie_response_data)
        session.add(favorite_movie_candidate)
        with pytest.raises(IntegrityError):
            await session.flush()
