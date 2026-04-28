from typing import Annotated, ClassVar

from annotated_types import Len, MaxLen
from pydantic import BaseModel, ConfigDict

from core.constants import (
    GENRE_DESCRIPTION_MAX_LENGTH,
    GENRE_NAME_MAX_LENGTH,
    GENRE_NAME_MIN_LENGTH,
)

NameConstraint = Annotated[
    str,
    Len(
        min_length=GENRE_NAME_MIN_LENGTH,
        max_length=GENRE_NAME_MAX_LENGTH,
    ),
]

DescriptionConstraint = Annotated[
    str,
    MaxLen(max_length=GENRE_DESCRIPTION_MAX_LENGTH),
]


class GenreBase(BaseModel):
    """
    Базовая модель для работы с жанром фильма.
    """

    name: NameConstraint
    description: DescriptionConstraint
    model_config: ClassVar[ConfigDict] = ConfigDict(from_attributes=True)


class GenreCreate(GenreBase):
    """
    Модель для создания жанра фильма.
    """


class GenreUpdate(GenreBase):
    """
    Модель для полного обновления информации о жанре фильма.
    """


class GenrePartialUpdate(BaseModel):
    """
    Модель для частичного обновления информации о жанре фильма.
    """

    name: NameConstraint | None = None
    description: DescriptionConstraint | None = None


class GenreResponse(GenreBase):
    """
    Модель для вывода информации о жанре фильма.
    """

    id: int


class GenreResponseList(BaseModel):
    """
    Модель для вывода информации о списке жанров.
    """

    genre_list: list[GenreResponse]
    size: int
    page: int
