from datetime import datetime
from typing import Annotated, ClassVar

from annotated_types import Len, MaxLen
from pydantic import BaseModel, ConfigDict, Field

NameString = Annotated[
    str,
    Len(min_length=3, max_length=20),
]

DescriptionString = Annotated[
    str,
    MaxLen(max_length=200),
]

RatingConstraint = Annotated[
    float,
    Field(
        ge=0.0,
        le=10.0,
    ),
]


class MovieBase(BaseModel):
    """
    Базовая модель для работы с фильмом.
    """

    name: NameString
    description: DescriptionString
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

    name: NameString | None = None
    description: DescriptionString | None = None
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
