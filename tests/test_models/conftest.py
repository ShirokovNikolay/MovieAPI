import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from models import Genre, Movie, User, Review, FavoriteMovie
from tests.test_schemas.test_genre import genre_data
from tests.test_schemas.test_movie import movie_data
from tests.test_schemas.test_user import user_data_encrypted_password
from tests.test_schemas.test_review import review_response_data
from tests.test_schemas.test_favorite_movie import favorite_movie_response_data


@pytest.fixture(scope="function")
async def genre(
    session: AsyncSession,
    genre_data: dict[str, str],
) -> Genre:
    genre_model = Genre(**genre_data)
    session.add(genre_model)
    await session.flush()
    await session.refresh(genre_model)
    return genre_model


@pytest.fixture(scope="function")
async def movie(
    session: AsyncSession,
    movie_data: dict,
    genre: Genre,
) -> Movie:
    movie_data["genre_id"] = genre.id
    movie_model = Movie(**movie_data)
    session.add(movie_model)
    await session.flush()
    await session.refresh(movie_model)
    return movie_model


@pytest.fixture(scope="function")
async def user(
    session: AsyncSession,
    user_data_encrypted_password: dict[str, str],
) -> User:
    user_model = User(**user_data_encrypted_password)
    session.add(user_model)
    await session.flush()
    await session.refresh(user_model)
    return user_model


@pytest.fixture(scope="function")
async def review(
    review_response_data: dict,
    movie: Movie,
    user: User,
    session: AsyncSession,
) -> Review:
    review_response_data["movie_id"] = movie.id
    review_response_data["user_id"] = user.id
    review_model = Review(**review_response_data)
    session.add(review_model)
    await session.flush()
    await session.refresh(review_model)
    return review_model


@pytest.fixture(scope="function")
async def favorite_movie(
    favorite_movie_response_data: dict,
    movie: Movie,
    user: User,
    session: AsyncSession,
) -> FavoriteMovie:
    favorite_movie_response_data["movie_id"] = movie.id
    favorite_movie_response_data["user_id"] = user.id
    favorite_movie_model = FavoriteMovie(**favorite_movie_response_data)
    session.add(favorite_movie_model)
    await session.flush()
    await session.refresh(favorite_movie_model)
    return favorite_movie_model
