import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from models import Genre, Movie
from schemas.genre import GenreCreate
from schemas.movie import MovieCreate
from tests.test_schemas.test_genre import genre_data
from tests.test_schemas.test_movie import movie_data


@pytest.fixture(scope="function")
def genre_create_schema(genre_data: dict[str, str]) -> GenreCreate:
    return GenreCreate(**genre_data)


@pytest.fixture(scope="function")
async def genre_model(
    session: AsyncSession,
    genre_create_schema: GenreCreate,
) -> Genre:
    genre = Genre(**genre_create_schema.model_dump())
    session.add(genre)
    await session.flush()
    await session.refresh(genre)
    return genre


@pytest.fixture(scope="function")
def movie_create_schema(movie_data: dict[str, str]) -> MovieCreate:
    return MovieCreate(**movie_data)


@pytest.fixture(scope="session")
async def movie_model(
    session: AsyncSession,
    movie_create_schema: MovieCreate,
    genre_model: Genre,
) -> Movie:
    movie_create_schema.genre_id = genre_model.id
    movie = Movie(**movie_create_schema.model_dump())
    session.add(movie)
    await session.flush()
    await session.refresh(movie)
    return movie
