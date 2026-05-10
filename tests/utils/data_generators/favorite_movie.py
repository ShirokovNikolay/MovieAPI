from schemas.favorite_movie import FavoriteMovieResponse
from tests.utils.data_generators.base import generate_number


def create_favorite_movie_data() -> dict[str, int]:
    data = {
        "movie_id": generate_number(),
    }
    return data


def create_favorite_movie_response_data() -> dict[str, int]:
    data = create_favorite_movie_data()
    data["id"] = generate_number()
    data["user_id"] = generate_number()
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
