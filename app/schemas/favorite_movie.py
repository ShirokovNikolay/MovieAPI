from typing import ClassVar

from pydantic import BaseModel, ConfigDict

from schemas.movie import MovieResponse


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
    user_id: int


class FavoriteMovieResponseList(BaseModel):
    """
    Модель для отображения списка избранных фильмов.
    """

    favorite_movie_list: list[FavoriteMovieResponse]
    size: int | None = None
    page: int | None = None


class FavoriteMovieWithMovieResponse(FavoriteMovieResponse):
    """
    Модель для вывода избранного фильма с подтягиванием данных о фильме.
    """

    movie: MovieResponse


class FavoriteMovieWithMovieResponseList(BaseModel):
    """
    Модель для отображения списка избранных фильмов c
    подтягиванием данных о фильме.
    """

    favorite_movie_list: list[FavoriteMovieWithMovieResponse]
    size: int | None = None
    page: int | None = None
