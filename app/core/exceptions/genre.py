from core.exceptions.base import NotFoundError, ConflictError


class GenreNotFoundError(NotFoundError):
    """
    Класс для ошибок, связанных с ненахождением жанра фильма.
    """

    def __init__(self, detail: str):
        super().__init__(detail)


class GenreIdNotFoundError(GenreNotFoundError):
    """
    Класс для ошибок, связанных с ненайденным id жанра фильма.
    """

    def __init__(self, genre_id):
        detail = f"Genre with genre id = {genre_id} doesn't exist."
        super().__init__(detail)


class GenreNameNotFoundError(GenreNotFoundError):
    """
    Класс для ошибок, связанных с ненайденным именем жанра фильма.
    """

    def __init__(self, genre_name: str):
        detail = f"Genre with genre name = {genre_name} doesn't exist."
        super().__init__(detail)


class GenreNameAlreadyExistsError(ConflictError):
    """
    Класс для ошибок, связанных с уже существующим именем жанра фильма.
    """

    def __init__(self, genre_name: str):
        detail = f"Genre with genre name = {genre_name} already exists."
        super().__init__(detail)
