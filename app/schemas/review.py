from datetime import datetime
from typing import Annotated, ClassVar

from annotated_types import MaxLen
from pydantic import BaseModel, ConfigDict, Field

from core.constants import (
    REVIEW_RATING_MAX_VALUE,
    REVIEW_RATING_MIN_VALUE,
    REVIEW_TEXT_MAX_LENGTH,
)

ReviewTextConstraint = Annotated[
    str,
    MaxLen(max_length=REVIEW_TEXT_MAX_LENGTH),
]
RatingConstraint = Annotated[
    int,
    Field(
        ge=REVIEW_RATING_MIN_VALUE,
        le=REVIEW_RATING_MAX_VALUE,
    ),
]


class ReviewBase(BaseModel):
    """
    Базовая модель для работы с отзывами.
    """

    review_text: ReviewTextConstraint
    rating: RatingConstraint
    movie_id: int
    model_config: ClassVar[ConfigDict] = ConfigDict(from_attributes=True)


class ReviewCreate(ReviewBase):
    """
    Модель для создания отзыва о фильме.
    """


class ReviewUpdate(BaseModel):
    """
    Модель для обновления отзыва о фильме.
    """

    review_text: ReviewTextConstraint
    rating: RatingConstraint


class ReviewPartialUpdate(BaseModel):
    """
    Модель для частичного обновления отзыва о фильме.
    """

    review_text: ReviewTextConstraint | None = None
    rating: RatingConstraint | None = None


class ReviewResponse(ReviewBase):
    """
    Модель для вывода информации об отзыве.
    """

    id: int
    user_id: int
    publication_date: datetime


class ReviewResponseList(BaseModel):
    """
    Модель для вывода списка отзывов.
    """

    review_list: list[ReviewResponse]
    size: int
    page: int
