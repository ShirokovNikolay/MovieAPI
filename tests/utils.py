import random
import string
from datetime import datetime

from faker import Faker

from schemas.favorite_movie import FavoriteMovieResponse
from schemas.genre import GenreResponse
from schemas.movie import MovieResponse
from schemas.review import ReviewResponse
from schemas.watch_history import WatchHistoryResponse
from core.constants import (
    MOVIE_NAME_MIN_LENGTH,
    MOVIE_NAME_MAX_LENGTH,
    MOVIE_DESCRIPTION_MIN_LENGTH,
    MOVIE_DESCRIPTION_MAX_LENGTH,
    MOVIE_RATING_MIN_VALUE,
    MOVIE_RATING_MAX_VALUE,
    REVIEW_TEXT_MIN_LENGTH,
    REVIEW_TEXT_MAX_LENGTH,
    REVIEW_RATING_MIN_VALUE,
    REVIEW_RATING_MAX_VALUE,
)


def generate_random_number(start=1, end=1000) -> int:
    return random.randint(start, end)


def generate_random_numbers(
    list_length: int = 5,
    start=1,
    end=1000,
) -> list[int]:
    return [generate_random_number(start, end) for _ in range(list_length)]


def generate_random_string(
    min_string_length: int = 1,
    max_string_length: int = 10,
    string_length: int | None = None,
) -> str:
    if string_length is None:
        string_length = random.randint(min_string_length, max_string_length)

    return "".join(
        [
            random.choice(
                string.ascii_letters + string.digits,
            )
            for _ in range(string_length)
        ],
    )


def generate_random_strings(
    min_string_length: int = 1,
    max_string_length: int = 10,
    string_length: int | None = None,
    min_list_length: int = 1,
    max_list_length: int = 5,
    list_length: int | None = None,
) -> list[str]:
    if list_length is None:
        list_length = random.randint(min_list_length, max_list_length)

    return [
        generate_random_string(
            min_string_length,
            max_string_length,
            string_length,
        )
        for _ in range(list_length)
    ]


def create_favorite_movie_data() -> dict[str, int]:
    data = {
        "movie_id": generate_random_number(),
    }
    return data


def create_favorite_movie_response_data() -> dict[str, int]:
    data = create_favorite_movie_data()
    data["id"] = generate_random_number()
    return data


def create_favorite_movie_response_list_data(
    list_length: int = 5,
) -> list[FavoriteMovieResponse]:
    result = []
    for i in range(list_length):
        data = create_favorite_movie_response_data()
        favorite_movie_response = FavoriteMovieResponse(**data)
        result.append(favorite_movie_response)
    return result


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


def create_movie_data() -> dict[str, str | datetime]:
    faker = Faker()
    data = {
        "name": generate_random_string(
            min_string_length=MOVIE_NAME_MIN_LENGTH,
            max_string_length=MOVIE_NAME_MAX_LENGTH,
        ),
        "description": generate_random_string(
            min_string_length=MOVIE_DESCRIPTION_MIN_LENGTH,
            max_string_length=MOVIE_DESCRIPTION_MAX_LENGTH,
        ),
        "rating": generate_random_number(MOVIE_RATING_MIN_VALUE, MOVIE_RATING_MAX_VALUE)
        / 10,
        "preview_url": faker.url(),
        "source_url": faker.url(),
        "genre_id": generate_random_number(0, 100),
        "release_date": datetime(
            year=generate_random_number(2020, 2025),
            month=generate_random_number(1, 12),
            day=generate_random_number(1, 28),
        ),
    }
    return data


def create_movie_response_data() -> dict[str, str | int | datetime]:
    data = create_movie_data()
    data["id"] = generate_random_number()
    return data


def create_movie_response_list(list_length: int = 5) -> list[MovieResponse]:
    result = []
    for i in range(list_length):
        movie_data = create_movie_response_data()
        movie_response_schema = MovieResponse(**movie_data)
        result.append(movie_response_schema)
    return result


def check_schema_not_none_fields_is_valid(schema, data) -> None:
    for field in schema.model_dump(exclude_none=True):
        assert getattr(schema, field) == data[field]


def create_review_data():
    data = {
        "review_text": generate_random_string(
            min_string_length=REVIEW_TEXT_MIN_LENGTH,
            max_string_length=REVIEW_TEXT_MAX_LENGTH,
        ),
        "rating": generate_random_number(
            start=MOVIE_RATING_MIN_VALUE,
            end=MOVIE_RATING_MAX_VALUE,
        ),
        "movie_id": generate_random_number(1, 1000),
    }
    return data


def create_review_response_data():
    data = create_review_data()
    data["id"] = generate_random_number(1, 1000)
    data["user_id"] = generate_random_number(1, 1000)
    data["publication_date"] = datetime(
        year=generate_random_number(2020, 2025),
        month=generate_random_number(1, 12),
        day=generate_random_number(1, 28),
    )

    return data


def create_review_response_list_data(list_length: int = 5) -> list[ReviewResponse]:
    result = []
    for i in range(list_length):
        review_data = create_review_response_data()
        review_response = ReviewResponse(**review_data)
        result.append(review_response)
    return result


def create_token_info_data():
    data = {
        "access_token": generate_random_string(),
        "refresh_token": generate_random_string(),
        "token_type": generate_random_string(),
    }
    return data


def create_watch_history_data() -> dict[str, int]:
    data = {
        "movie_id": generate_random_number(1, 1000),
    }
    return data


def create_watch_history_response_data() -> dict[str, str | int | datetime]:
    data = create_watch_history_data()
    data["id"] = generate_random_number()
    data["user_id"] = generate_random_number()
    data["watched_at"] = datetime(
        year=generate_random_number(2020, 2025),
        month=generate_random_number(1, 12),
        day=generate_random_number(1, 28),
    )
    return data


def create_watch_history_response_list(
    list_length: int = 5,
) -> list[WatchHistoryResponse]:
    result = []
    for i in range(list_length):
        watch_history_data = create_watch_history_response_data()
        watch_history_response = WatchHistoryResponse(**watch_history_data)
        result.append(watch_history_response)
    return result
