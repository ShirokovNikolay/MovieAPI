from datetime import datetime
from typing import Annotated, ClassVar

from annotated_types import MaxLen
from pydantic import BaseModel, ConfigDict, Field

StringMaxLength400 = Annotated[
    str,
    MaxLen(max_length=400),
]
RatingConstraint = Annotated[
    int,
    Field(ge=0, le=10),
]


class ReviewBase(BaseModel):
    """
    Базовая модель для работы с отзывами.
    """

    review_text: StringMaxLength400
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

    review_text: StringMaxLength400
    rating: RatingConstraint


class ReviewPartialUpdate(BaseModel):
    """
    Модель для частичного обновления отзыва о фильме.
    """

    review_text: StringMaxLength400 | None = None
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
