from typing import Annotated, ClassVar

from annotated_types import Len, MaxLen
from pydantic import BaseModel, ConfigDict

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
    Базовая модель для работы с жанром фильма.
    """

    name: NameString
    description: DescriptionString
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

    name: NameString | None = None
    description: DescriptionString | None = None


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
    page: int = 1
