from typing import ClassVar

from pydantic import BaseModel, ConfigDict


class FavoriteMovieBase(BaseModel):
    """
    Базовая модель для использования фильма в качестве
    избранного для заданного пользователя.
    """

    movie_id: int
    model_config: ClassVar[ConfigDict] = ConfigDict(from_attributes=True)


class FavoriteMovieCreate(FavoriteMovieBase):
    """
    Модель для добавления фильма в список избранных в для заданного пользователя.
    """


class FavoriteMovieResponse(FavoriteMovieBase):
    """
    Модель для вывода данных об избранном фильма для заданного пользователя.
    """

    id: int


class FavoriteMovieResponseList(BaseModel):
    """
    Модель для отображения списка избранных фильмов.
    """

    favorite_movie_list: list[FavoriteMovieResponse]
    size: int
    page: int
