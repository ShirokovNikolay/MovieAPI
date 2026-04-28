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
from core.constants import (
    REVIEW_TEXT_MAX_LENGTH,
    REVIEW_RATING_MIN_VALUE,
    REVIEW_RATING_MAX_VALUE,
)
from tests.utils import (
    generate_random_string,
    generate_random_number,
    create_review_data,
    create_review_response_data,
    create_review_response_list_data,
)


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
        review_response_data["rating"] = REVIEW_RATING_MIN_VALUE - 1
        with pytest.raises(ValidationError):
            schema(**review_response_data)

    def test_review_with_too_large_rating_field(
        self,
        schema,
        review_response_data: dict[str, str | int],
    ) -> None:
        review_response_data["rating"] = REVIEW_RATING_MAX_VALUE + 1
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

    def test_review_response_list_schema_with_empty_list(self) -> None:
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
