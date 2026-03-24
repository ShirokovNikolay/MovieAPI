from datetime import datetime
from typing import Annotated

from annotated_types import Len, MaxLen
from pydantic import BaseModel, Field, ConfigDict

NameString = Annotated[
    str,
    Len(min_length=3, max_length=20),
]

DescriptionString = Annotated[
    str,
    MaxLen(max_length=200),
]

RatingConstarint = Annotated[
    float,
    Field(
        ge=0.0,
        le=10.0,
    ),
]


class MovieBase(BaseModel):
    """
    Базовый класс для работы с фильмом.
    """

    model_config: ConfigDict = ConfigDict(from_attributes=True)
    name: NameString
    description: DescriptionString
    rating: RatingConstarint
    preview_url: str
    source_url: str
    genre_id: int
    release_date: datetime


class MovieCreate(MovieBase):
    """
    Класс для создания фильма.
    """


class MovieUpdate(MovieBase):
    """
    Класс для обновления фильма.
    """


class MoviePartialUpdate(MovieBase):
    """
    Класс для частичного обновления фильма.
    """

    name: NameString | None = None
    description: DescriptionString | None = None
    rating: RatingConstarint | None = None
    preview_url: str | None = None
    source_url: str | None = None
    genre_id: int | None = None
    release_date: datetime | None = None


class MovieResponse(MovieBase):
    """
    Класс для вывода информации о фильме.
    """

    id: int


class MovieResponseList(MovieResponse):
    """
    Класс для вывода информации о списке фильмов.
    """

    movie_list: list[MovieResponse]
