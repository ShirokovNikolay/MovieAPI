from datetime import datetime

import pytest
from pydantic import ValidationError

from schemas.review import (
    ReviewBase,
    ReviewResponse,
    ReviewCreate,
    ReviewUpdate,
    ReviewPartialUpdate,
    ReviewResponseList,
)
from tests.utils import generate_random_string, generate_random_number

REVIEW_TEXT_MIN_LENGTH = 0
REVIEW_TEXT_MAX_LENGTH = 400
RATING_MIN_VALUE = 0
RATING_MAX_VALUE = 10


def create_review_data():
    data = {
        "review_text": generate_random_string(
            min_string_length=REVIEW_TEXT_MIN_LENGTH,
            max_string_length=REVIEW_TEXT_MAX_LENGTH,
        ),
        "rating": generate_random_number(
            start=RATING_MIN_VALUE,
            end=RATING_MAX_VALUE,
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


@pytest.fixture(scope="function")
def review_data():
    return create_review_data()


@pytest.fixture(scope="function")
def review_response_data():
    return create_review_response_data()


@pytest.fixture(scope="function")
def review_response_list() -> list[ReviewResponse]:
    return create_review_response_list_data(list_length=3)


@pytest.mark.parametrize(
    "schema",
    [
        ReviewBase,
        ReviewCreate,
        ReviewUpdate,
        ReviewResponse,
    ],
)
class TestReviewBaseCreateUpdateResponse:
    def test_review(
        self,
        schema,
        review_response_data: dict[str, str | int],
    ) -> None:
        schema_object = schema(**review_response_data)
        for field in schema_object.model_dump():
            assert getattr(schema_object, field) == review_response_data[field]

    def test_review_without_text(
        self,
        schema,
        review_response_data: dict[str, str | int],
    ) -> None:
        review_response_data.pop("review_text")
        with pytest.raises(ValidationError, match="Field required"):
            schema(**review_response_data)

    def test_review_without_rating(
        self,
        schema,
        review_response_data: dict[str, str | int],
    ) -> None:
        review_response_data.pop("rating")
        with pytest.raises(ValidationError, match="Field required"):
            schema(**review_response_data)

    def test_review_without_movie_id(
        self,
        schema,
        review_response_data: dict[str, str | int],
    ) -> None:
        if schema is ReviewUpdate:
            pytest.skip(
                reason="ReviewUpdate should not have movie_id field but should test ReviewUpdate schema due to DRY principe",
            )
        review_response_data.pop("movie_id")
        with pytest.raises(ValidationError, match="Field required"):
            schema(**review_response_data)

    def test_review_with_too_long_text_field(
        self,
        schema,
        review_response_data: dict[str, str | int],
    ) -> None:
        review_response_data["review_text"] = generate_random_string(
            string_length=REVIEW_TEXT_MAX_LENGTH + 1,
        )
        with pytest.raises(ValidationError, match="string_too_long"):
            schema(**review_response_data)

    def test_review_with_too_small_rating_field(
        self,
        schema,
        review_response_data: dict[str, str | int],
    ) -> None:
        review_response_data["rating"] = RATING_MIN_VALUE - 1
        with pytest.raises(ValidationError):
            schema(**review_response_data)

    def test_review_with_too_large_rating_field(
        self,
        schema,
        review_response_data: dict[str, str | int],
    ) -> None:
        review_response_data["rating"] = RATING_MAX_VALUE + 1
        with pytest.raises(ValidationError):
            schema(**review_response_data)


class TestReviewPartialUpdate:
    def test_review_partial_update(
        self,
        review_data: dict[str, str | int],
    ) -> None:
        schema_object = ReviewPartialUpdate(**review_data)
        for field in schema_object.model_dump():
            assert getattr(schema_object, field) == review_data[field]

    def test_review_partial_update_without_text(
        self,
        review_data: dict[str, str | int],
    ) -> None:
        review_data.pop("review_text")
        review_partial_update_schema = ReviewPartialUpdate(**review_data)
        assert review_partial_update_schema.review_text is None
        assert review_partial_update_schema.rating == review_data["rating"]

    def test_review_partial_update_without_rating(
        self,
        review_data: dict[str, str | int],
    ) -> None:
        review_data.pop("rating")
        review_partial_update_schema = ReviewPartialUpdate(**review_data)
        assert review_partial_update_schema.review_text == review_data["review_text"]
        assert review_partial_update_schema.rating is None


class TestReviewResponseList:
    def test_review_response_list(
        self,
        review_response_list: list[ReviewResponse],
    ) -> None:
        page = generate_random_number()
        size = generate_random_number()
        schema = ReviewResponseList(
            review_list=review_response_list,
            page=page,
            size=size,
        )
        assert schema.review_list == review_response_list
        assert schema.page == page
        assert schema.size == size

    def test_review_response_list_schema_with_empty_genre_list(self) -> None:
        page = generate_random_number()
        size = generate_random_number()
        schema = ReviewResponseList(
            review_list=[],
            page=page,
            size=size,
        )
        assert len(schema.review_list) == 0
        assert schema.page == page
        assert schema.size == size
