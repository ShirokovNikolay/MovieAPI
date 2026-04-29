from schemas.genre import GenreResponse
from tests.utils.data_generators.base import generate_string, generate_number


def create_genre_data() -> dict[str, str]:
    data = {
        "name": generate_string(
            min_string_length=3,
            max_string_length=15,
        ),
        "description": generate_string(
            min_string_length=0,
            max_string_length=200,
        ),
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
