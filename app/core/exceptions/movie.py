from core.exceptions.base import ConflictError, NotFoundError


class MovieNotFoundError(NotFoundError):
    """
    Класс для ошибок, связанных с ненахождением фильма.
    """

    def __init__(self, detail: str) -> None:
        super().__init__(detail)


class MovieIdNotFoundError(MovieNotFoundError):
    """
    Класс для ошибок, связанных с ненахождением id фильма.
    """

    def __init__(self, movie_id: int) -> None:
        self.movie_id = movie_id
        detail = f"Movie with movie id = {movie_id} not found."
        super().__init__(detail)


class MovieAlreadyExistsError(ConflictError):
    """
    Класс для ошибок из-за ненахождения фильма.
    """

    def __init__(self, detail: str) -> None:
        super().__init__(detail)


class MovieNameAlreadyExistsError(MovieAlreadyExistsError):
    """
    Класс для ошибок, связанных с уже существующим именем фильма.
    """

    def __init__(self, movie_name: str) -> None:
        self.movie_name = movie_name
        detail = f"Movie with movie name = {movie_name} already exists."
        super().__init__(detail)
