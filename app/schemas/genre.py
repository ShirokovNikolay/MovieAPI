from typing import Annotated

from annotated_types import Len, MaxLen
from pydantic import BaseModel


NameString = Annotated[
    str,
    Len(min_length=3, max_length=15),
]

DescriptionString = Annotated[
    str,
    MaxLen(max_length=200),
]


class GenreBase(BaseModel):
    """
    Базовый класс для работы с жанром фильма.
    """

    name: NameString
    description: DescriptionString


class GenreCreate(GenreBase):
    """
    Класс для создания жанра фильма.
    """


class GenreUpdate(GenreBase):
    """
    Класс для полного обновления информации о жанре фильма.
    """


class GenrePartialUpdate(GenreBase):
    """
    Класс для частичного обновления информации о жанре фильма.
    """

    name: NameString | None = None
    description: DescriptionString | None = None


class GenreResponse(GenreBase):
    """
    Класс для вывода информации о жанре фильма.
    """

    id: int
