import pytest
from sqlalchemy.exc import DBAPIError
from sqlalchemy.ext.asyncio import AsyncSession

from core.constants import (
    REVIEW_RATING_MIN_VALUE,
    REVIEW_RATING_MAX_VALUE,
    REVIEW_TEXT_MAX_LENGTH,
)
from models import Movie, User, Review
from tests.utils.data_generators.base import generate_number, generate_string


class TestReviewModel:
    async def test_create_review(
        self,
        review_response_data: dict,
        movie_model: Movie,
        user_model: User,
        session: AsyncSession,
    ) -> None:
        review_response_data["movie_id"] = movie_model.id
        review_response_data["user_id"] = user_model.id
        review = Review(**review_response_data)
        session.add(review)
        await session.flush()
        await session.refresh(review)

        assert review.movie_id == review_response_data["movie_id"]
        assert review.user_id == review_response_data["user_id"]
        assert review.review_text == review_response_data["review_text"]
        assert review.rating == review_response_data["rating"]
        assert review.publication_date == review_response_data["publication_date"]

    @pytest.mark.parametrize(
        "field,value,expected_error",
        [
            (
                "user_id",
                generate_number(start=-100, end=-1),
                DBAPIError,
            ),
            (
                "movie_id",
                generate_number(start=-100, end=-1),
                DBAPIError,
            ),
            (
                "review_text",
                generate_string(length=REVIEW_TEXT_MAX_LENGTH + 1),
                DBAPIError,
            ),
            (
                "rating",
                REVIEW_RATING_MIN_VALUE - 1,
                DBAPIError,
            ),
            (
                "rating",
                REVIEW_RATING_MAX_VALUE + 1,
                DBAPIError,
            ),
        ],
    )
    async def test_field_constraints_with_wrong_data(
        self,
        session: AsyncSession,
        review_model: Review,
        field: str,
        value: str | int,
        expected_error,
    ) -> None:
        setattr(review_model, field, value)
        with pytest.raises(expected_error):
            await session.flush()
