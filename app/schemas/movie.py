from datetime import date
from typing import ClassVar

from pydantic import BaseModel, ConfigDict

from core.constants import (
    SortMonotony,
    SortType,
)
from schemas.constraints.movie import (
    DescriptionConstraint,
    NameConstraint,
    RatingConstraint,
)
from schemas.genre import GenreResponse


class MovieBase(BaseModel):
    """
    Базовая модель для работы с фильмом.
    """

    name: NameConstraint
    description: DescriptionConstraint
    rating: RatingConstraint
    preview_url: str
    source_url: str
    genre_id: int
    release_date: date
    model_config: ClassVar[ConfigDict] = ConfigDict(from_attributes=True)


class MovieCreate(MovieBase):
    """
    Модель для создания фильма.
    """


class MovieUpdate(MovieBase):
    """
    Модель для обновления фильма.
    """


class MoviePartialUpdate(BaseModel):
    """
    Модель для частичного обновления фильма.
    """

    name: NameConstraint | None = None
    description: DescriptionConstraint | None = None
    rating: RatingConstraint | None = None
    preview_url: str | None = None
    source_url: str | None = None
    genre_id: int | None = None
    release_date: date | None = None


class MovieResponse(MovieBase):
    """
    Модель для вывода информации о фильме.
    """

    id: int


class MovieResponseList(BaseModel):
    """
    Модель для вывода информации о списке фильмов.
    """

    movie_list: list[MovieResponse]
    size: int | None = None
    page: int | None = None


class MovieWithGenreResponse(MovieResponse):
    """
    Модель для вывода информации о фильме, включая данные о его жанре.
    """

    genre: GenreResponse


class MovieWithGenreResponseList(BaseModel):
    """
    Модель для вывода информации о списке фильмов, включая их жанры.
    """

    movie_list: list[MovieWithGenreResponse]
    size: int
    page: int


class MovieFilter(BaseModel):
    """
    Модель для принятия данных о поиске, фильтрации и сортировке фильмов.
    """

    min_rating: RatingConstraint | None = None
    max_rating: RatingConstraint | None = None
    start_release_date: date | None = None
    end_release_date: date | None = None
    genre_id: int | None = None
    search_query: str | None = None
    sort_by: SortType | None = None
    sorting_direction: SortMonotony = SortMonotony.ascending.value  # type: ignore # noqa: PGH003
