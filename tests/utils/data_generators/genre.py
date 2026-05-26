from core.constants import (
    GENRE_NAME_MIN_LENGTH,
    GENRE_NAME_MAX_LENGTH,
    GENRE_DESCRIPTION_MAX_LENGTH,
    GENRE_DESCRIPTION_MIN_LENGTH,
)
from schemas.genre import GenreResponse
from tests.utils.data_generators.base import generate_string, generate_number
from faker import Faker


def create_genre_data() -> dict[str, str]:
    fake = Faker()
    data = {
        "name": generate_string(
            min_string_length=GENRE_NAME_MIN_LENGTH,
            max_string_length=GENRE_NAME_MAX_LENGTH,
        ),
        "description": generate_string(
            min_string_length=GENRE_DESCRIPTION_MIN_LENGTH,
            max_string_length=GENRE_DESCRIPTION_MAX_LENGTH,
        ),
        "preview_url": fake.url(),
    }
    return data


def create_genre_response_data() -> dict[str, str | int]:
    data = create_genre_data()
    data["id"] = generate_number()
    return data


def create_genre_response_list(list_length: int = 5) -> list[GenreResponse]:
    genre_response_list = []
    for i in range(list_length):
        genre_data = create_genre_response_data()
        genre_response = GenreResponse(**genre_data)
        genre_response_list.append(genre_response)
    return genre_response_list
