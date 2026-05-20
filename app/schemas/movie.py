from datetime import date, datetime
from typing import Annotated, ClassVar

from annotated_types import Len, MaxLen
from pydantic import BaseModel, ConfigDict, Field

from core.constants import (
    MOVIE_DESCRIPTION_MAX_LENGTH,
    MOVIE_NAME_MAX_LENGTH,
    MOVIE_NAME_MIN_LENGTH,
    MOVIE_RATING_MAX_VALUE,
    MOVIE_RATING_MIN_VALUE,
    SortMonotony,
    SortType,
)
from schemas.genre import GenreResponse

NameConstraint = Annotated[
    str,
    Len(
        min_length=MOVIE_NAME_MIN_LENGTH,
        max_length=MOVIE_NAME_MAX_LENGTH,
    ),
]

DescriptionConstraint = Annotated[
    str,
    MaxLen(max_length=MOVIE_DESCRIPTION_MAX_LENGTH),
]

RatingConstraint = Annotated[
    float,
    Field(
        ge=MOVIE_RATING_MIN_VALUE,
        le=MOVIE_RATING_MAX_VALUE,
    ),
]


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
    release_date: datetime
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
    release_date: datetime | None = None


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
    size: int
    page: int


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
