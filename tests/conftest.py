from datetime import datetime
from os import getenv
from typing import AsyncGenerator

import pytest
from sqlalchemy.ext.asyncio import AsyncSession


from core.database.connection import session_factory
from core.security.password_utils import hash_password
from schemas.favorite_movie import FavoriteMovieResponse
from schemas.genre import GenreResponse
from schemas.review import ReviewResponse
from schemas.user import UserResponse
from schemas.watch_history import WatchHistoryResponse
from tests.utils.data_generators.favorite_movie import (
    create_favorite_movie_response_data,
    create_favorite_movie_response_list_data,
)
from tests.utils.data_generators.genre import (
    create_genre_data,
    create_genre_response_data,
    create_genre_response_list,
)
from tests.utils.data_generators.movie import (
    create_movie_data,
    create_movie_response_data,
    create_movie_response_list,
)
from tests.utils.data_generators.review import (
    create_review_data,
    create_review_response_data,
    create_review_response_list_data,
)
from tests.utils.data_generators.user import (
    create_user_data,
    create_user_response_data,
    create_user_response_list,
)
from tests.utils.data_generators.watch_history import (
    create_watch_history_data,
    create_watch_history_response_data,
    create_watch_history_response_list,
)


@pytest.fixture(scope="session", autouse=True)
def test_environment_is_ready() -> None:
    if getenv("TESTING") != "1":
        pytest.exit(
            reason="Environment is not ready!",
        )


@pytest.fixture(scope="function")
async def session() -> AsyncGenerator[AsyncSession, None]:
    async with session_factory() as db_session:
        yield db_session
        await db_session.rollback()


@pytest.fixture(scope="function")
def genre_data() -> dict[str, str]:
    return create_genre_data()


@pytest.fixture(scope="function")
def genre_response_data() -> dict[str, str | int]:
    return create_genre_response_data()


@pytest.fixture(scope="function")
def genre_response_list() -> list[GenreResponse]:
    return create_genre_response_list(list_length=3)


@pytest.fixture(scope="function")
def movie_data():
    return create_movie_data()


@pytest.fixture(scope="function")
def movie_response_data():
    return create_movie_response_data()


@pytest.fixture(scope="function")
def movie_response_list():
    return create_movie_response_list(list_length=3)


@pytest.fixture(scope="function")
def user_data() -> dict[str, str]:
    return create_user_data()


@pytest.fixture(scope="function")
def user_data_encrypted_password() -> dict[str, str]:
    data = create_user_data()
    password = data.pop("password")
    data["encrypted_password"] = hash_password(password)
    return data


@pytest.fixture(scope="function")
def user_response_data() -> dict[str, str | int]:
    return create_user_response_data()


@pytest.fixture(scope="function")
def user_response_list() -> list[UserResponse]:
    return create_user_response_list(list_length=3)


@pytest.fixture(scope="function")
def review_data():
    return create_review_data()


@pytest.fixture(scope="function")
def review_response_data():
    return create_review_response_data()


@pytest.fixture(scope="function")
def review_response_list() -> list[ReviewResponse]:
    return create_review_response_list_data(list_length=3)


@pytest.fixture(scope="function")
def watch_history_data() -> dict[str, int]:
    return create_watch_history_data()


@pytest.fixture(scope="function")
def favorite_movie_response_data() -> dict[str, int]:
    return create_favorite_movie_response_data()


@pytest.fixture(scope="function")
def favorite_movie_response_list() -> list[FavoriteMovieResponse]:
    return create_favorite_movie_response_list_data(list_length=3)


@pytest.fixture(scope="function")
def watch_history_response_data() -> dict[str, str | int | datetime]:
    return create_watch_history_response_data()


@pytest.fixture(scope="function")
def watch_history_response_list() -> list[WatchHistoryResponse]:
    return create_watch_history_response_list(list_length=3)
