from typing import ClassVar

from pydantic import BaseModel, ConfigDict

from schemas.constraints.genre import DescriptionConstraint, NameConstraint


class GenreBase(BaseModel):
    """
    Базовая модель для работы с жанром фильма.
    """

    name: NameConstraint
    description: DescriptionConstraint
    preview_url: str
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
    preview_url: str | None = None


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
    size: int | None = None
    page: int | None = None
