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
from tests.utils.data_generators.base import (
    generate_string,
    generate_number,
    check_schema_not_none_fields_is_valid,
)
from tests.utils.data_generators.review import (
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
        ReviewPartialUpdate,
        ReviewResponse,
    ],
)
class TestReviewBaseCreateUpdatePartialUpdateResponse:
    def test_review(
        self,
        schema,
        review_response_data: dict[str, str | int],
    ) -> None:
        schema_object = schema(**review_response_data)
        for field in schema_object.model_dump():
            assert getattr(schema_object, field) == review_response_data[field]

    @pytest.mark.parametrize(
        "field",
        [
            "review_text",
            "movie_id",
            "rating",
        ],
    )
    def test_review_without_field(
        self,
        schema,
        field: str,
        review_response_data: dict[str, str | int],
    ) -> None:
        if schema is ReviewPartialUpdate:
            pytest.skip(
                reason="Review Partial Update schema does not have required fields"
            )
        if field == "movie_id" and schema is ReviewUpdate:
            pytest.skip(
                reason="Review Update schema does not have required movie_id field"
            )
        review_response_data.pop(field)
        with pytest.raises(ValidationError, match="Field required"):
            schema(**review_response_data)

    @pytest.mark.parametrize(
        "field,value,expected_error_message",
        [
            (
                "review_text",
                generate_string(length=REVIEW_TEXT_MAX_LENGTH + 1),
                "string_too_long",
            ),
            (
                "rating",
                REVIEW_RATING_MIN_VALUE - 1,
                "greater_than_equal",
            ),
            (
                "rating",
                REVIEW_RATING_MAX_VALUE + 1,
                "less_than_equal",
            ),
        ],
    )
    def test_review_with_not_valid_field_value(
        self,
        schema,
        field: str,
        value: str | int,
        expected_error_message: str,
        review_response_data: dict[str, str | int],
    ) -> None:
        review_response_data[field] = value
        with pytest.raises(ValidationError, match=expected_error_message):
            schema(**review_response_data)


class TestReviewPartialUpdate:
    def test_review_without_field(
        self,
        review_data: dict[str, str | int],
    ) -> None:
        review_data_copy = review_data.copy()
        review_data_copy.pop("movie_id")
        for field in review_data_copy:
            value = review_data.pop(field)
            review_update_schema = ReviewPartialUpdate(**review_data)
            check_schema_not_none_fields_is_valid(
                review_update_schema,
                review_data,
            )
            assert getattr(review_update_schema, field) is None
            review_data[field] = value


class TestReviewResponseList:
    def test_review_response_list(
        self,
        review_response_list: list[ReviewResponse],
    ) -> None:
        page = generate_number()
        size = generate_number()
        schema = ReviewResponseList(
            review_list=review_response_list,
            page=page,
            size=size,
        )
        assert schema.review_list == review_response_list
        assert schema.page == page
        assert schema.size == size

    def test_review_response_list_schema_with_empty_list(self) -> None:
        page = generate_number()
        size = generate_number()
        schema = ReviewResponseList(
            review_list=[],
            page=page,
            size=size,
        )
        assert len(schema.review_list) == 0
        assert schema.page == page
        assert schema.size == size
