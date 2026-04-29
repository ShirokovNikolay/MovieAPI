from datetime import datetime

from core.constants import (
    REVIEW_TEXT_MIN_LENGTH,
    REVIEW_TEXT_MAX_LENGTH,
    MOVIE_RATING_MIN_VALUE,
    MOVIE_RATING_MAX_VALUE,
)
from schemas.review import ReviewResponse
from tests.utils.data_generators.base import generate_string, generate_number


def create_review_data():
    data = {
        "review_text": generate_string(
            min_string_length=REVIEW_TEXT_MIN_LENGTH,
            max_string_length=REVIEW_TEXT_MAX_LENGTH,
        ),
        "rating": generate_number(
            start=MOVIE_RATING_MIN_VALUE,
            end=MOVIE_RATING_MAX_VALUE,
        ),
        "movie_id": generate_number(1, 1000),
    }
    return data


def create_review_response_data():
    data = create_review_data()
    data["id"] = generate_number(1, 1000)
    data["user_id"] = generate_number(1, 1000)
    data["publication_date"] = datetime(
        year=generate_number(2020, 2025),
        month=generate_number(1, 12),
        day=generate_number(1, 28),
    )

    return data


def create_review_response_list_data(list_length: int = 5) -> list[ReviewResponse]:
    result = []
    for i in range(list_length):
        review_data = create_review_response_data()
        review_response = ReviewResponse(**review_data)
        result.append(review_response)
    return result
