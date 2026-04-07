from core.exceptions.base import NotFoundError, ConflictError


class MovieNotFoundError(NotFoundError):
    """
    Класс для ошибок, связанных с ненахождением фильма.
    """

    def __init__(self, detail: str):
        super().__init__(detail)


class MovieIdNotFoundError(MovieNotFoundError):
    """
    Класс для ошибок, связанных с ненахождением id фильма.
    """

    def __init__(self, movie_id: int):
        detail = f"Movie with movie id = {movie_id} not found."
        super().__init__(detail)


class MovieNameNotFoundError(MovieNotFoundError):
    """
    Класс для ошибок, связанных с ненахождением имени фильма.
    """

    def __init__(self, movie_name: str):
        detail = f"Movie with movie name = {movie_name} not found."
        super().__init__(detail)


class MovieNameAlreadyExistsError(ConflictError):
    """
    Класс для ошибок, связанных с уже существующим именем фильма.
    """

    def __init__(self, movie_name: str):
        detail = f"Movie with movie name = {movie_name} already exists."
        super().__init__(detail)
