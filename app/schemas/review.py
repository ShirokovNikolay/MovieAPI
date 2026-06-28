from datetime import datetime
from typing import ClassVar

from pydantic import BaseModel, ConfigDict

from schemas.constraints.review import RatingConstraint, ReviewTextConstraint
from schemas.movie import MovieResponse
from schemas.user import UserResponse


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


class ReviewWithUserResponse(ReviewResponse):
    """
    Модель для вывода информации об отзыве вместе с пользователем.
    """

    user: UserResponse


class ReviewWithUserResponseList(BaseModel):
    """
    Модель для вывода списка отзывов вместе с пользователем.
    """

    review_list: list[ReviewWithUserResponse]
    size: int
    page: int


class ReviewWithMovieResponse(ReviewResponse):
    """
    Модель для вывода данных об отзыве с информацией о фильме.
    """

    movie: MovieResponse


class ReviewWithMovieResponseList(BaseModel):
    """
    Модель для вывода списка отзывов вместе с фильмом.
    """

    review_list: list[ReviewWithMovieResponse]
    size: int
    page: int
