from typing import Annotated

from annotated_types import MaxLen
from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime


StringMaxLength400 = Annotated[str, MaxLen(max_length=400)]
RatingConstarint = Annotated[
    int,
    Field(ge=0, le=10),
]


class ReviewBase(BaseModel):
    """
    Базовая модель для работы с отзывами.
    """

    review_text: StringMaxLength400
    rating: RatingConstarint
    model_config: ConfigDict = ConfigDict(from_attributes=True)


class ReviewCreate(ReviewBase):
    """
    Модель для создания отзыва о фильме.
    """

    movie_id: int


class ReviewUpdate(ReviewBase):
    """
    Модель для обновления отзыва о фильме.
    """


class ReviewPartialUpdate(ReviewBase):
    """
    Модель для частичного обновления отзыва о фильме.
    """

    review_text: StringMaxLength400 | None = None
    rating: RatingConstarint | None = None


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
    page: int = 1
