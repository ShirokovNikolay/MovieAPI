import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from models import Genre, Movie, User, Review
from tests.test_schemas.test_genre import genre_data
from tests.test_schemas.test_movie import movie_data
from tests.test_schemas.test_user import user_data_encrypted_password
from tests.test_schemas.test_review import review_response_data


@pytest.fixture(scope="function")
async def genre_model(
    session: AsyncSession,
    genre_data: dict[str, str],
) -> Genre:
    genre = Genre(**genre_data)
    session.add(genre)
    await session.flush()
    await session.refresh(genre)
    return genre


@pytest.fixture(scope="function")
async def movie_model(
    session: AsyncSession,
    movie_data: dict,
    genre_model: Genre,
) -> Movie:
    movie_data["genre_id"] = genre_model.id
    movie = Movie(**movie_data)
    session.add(movie)
    await session.flush()
    await session.refresh(movie)
    return movie


@pytest.fixture(scope="function")
async def user_model(
    session: AsyncSession,
    user_data_encrypted_password: dict[str, str],
) -> User:
    user = User(**user_data_encrypted_password)
    session.add(user)
    await session.flush()
    await session.refresh(user)
    return user


@pytest.fixture(scope="function")
async def review_model(
    review_response_data: dict,
    movie_model: Movie,
    user_model: User,
    session: AsyncSession,
) -> Review:
    review_response_data["movie_id"] = movie_model.id
    review_response_data["user_id"] = user_model.id
    review_model = Review(**review_response_data)
    session.add(review_model)
    await session.flush()
    await session.refresh(review_model)
    return review_model
