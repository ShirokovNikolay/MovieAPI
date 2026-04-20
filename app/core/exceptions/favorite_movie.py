from core.exceptions.base import ConflictError, NotFoundError


class FavoriteMovieNotFoundError(NotFoundError):
    """
    Класс для ошибок из-за ненахождения фильма в избранных для пользователя.
    """

    def __init__(self, detail: str):
        super().__init__(detail)


class FavoriteMovieIdNotFoundError(FavoriteMovieNotFoundError):
    """
    Класс для ошибок из-за ненахождения фильма в избранных для пользователя по id.
    """

    def __init__(self, favorite_movie_id: int):
        detail = f"Favorite movie with id = {favorite_movie_id} not found."
        super().__init__(detail)


class FavoriteMovieNotFoundByUserAndMovieError(FavoriteMovieNotFoundError):
    """
    Класс для ошибок из-за ненахождения фильма в избранных
    для пользователя по id пользователя и фильма.
    """

    def __init__(self, user_id: int, movie_id: int):
        detail = f"Favorite movie with user_id = {user_id} and movie_id = {movie_id} not found."
        super().__init__(detail)


class FavoriteMovieAlreadyExistsByUserAndMovieError(ConflictError):
    """
    Класс для ошибок из-за существования фильма в избранных для пользователя.
    """

    def __init__(self, user_id: int, movie_id: int):
        detail = f"Favorite movie with user_id = {user_id} and movie_id = {movie_id} already exists."
        super().__init__(detail)
