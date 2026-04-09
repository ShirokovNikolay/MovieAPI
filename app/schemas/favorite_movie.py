from pydantic import BaseModel


class FavoriteMovieBase(BaseModel):
    """
    Базовая модель для использования фильма в качестве избранного для заданного пользователя.
    """

    movie_id: int


class FavoriteMovieCreate(FavoriteMovieBase):
    """
    Модель для добавления фильма в список избранных в для заданного пользователя.
    """


class FavoriteMovieResponse(FavoriteMovieBase):
    """
    Модель для вывода данных об избранном фильма для заданного пользователя.
    """

    id: int
