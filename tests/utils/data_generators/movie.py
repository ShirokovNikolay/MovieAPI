from datetime import date

from faker import Faker

from core.constants import (
    MOVIE_NAME_MIN_LENGTH,
    MOVIE_NAME_MAX_LENGTH,
    MOVIE_DESCRIPTION_MIN_LENGTH,
    MOVIE_DESCRIPTION_MAX_LENGTH,
    MOVIE_RATING_MIN_VALUE,
    MOVIE_RATING_MAX_VALUE,
)
from schemas.movie import MovieResponse
from tests.utils.data_generators.base import generate_string, generate_number


def create_movie_data() -> dict[str, str | date]:
    faker = Faker()
    data = {
        "name": generate_string(
            min_string_length=MOVIE_NAME_MIN_LENGTH,
            max_string_length=MOVIE_NAME_MAX_LENGTH,
        ),
        "description": generate_string(
            min_string_length=MOVIE_DESCRIPTION_MIN_LENGTH,
            max_string_length=MOVIE_DESCRIPTION_MAX_LENGTH,
        ),
        "rating": generate_number(
            10 * MOVIE_RATING_MIN_VALUE, 10 * MOVIE_RATING_MAX_VALUE
        )
        / 10,
        "preview_url": faker.url(),
        "source_url": faker.url(),
        "genre_id": generate_number(0, 100),
        "release_date": date(
            year=generate_number(2020, 2025),
            month=generate_number(1, 12),
            day=generate_number(1, 28),
        ),
    }
    return data


def create_movie_response_data() -> dict[str, str | int | date]:
    data = create_movie_data()
    data["id"] = generate_number()
    return data


def create_movie_response_list(list_length: int = 5) -> list[MovieResponse]:
    result = []
    for i in range(list_length):
        movie_data = create_movie_response_data()
        movie_response_schema = MovieResponse(**movie_data)
        result.append(movie_response_schema)
    return result
