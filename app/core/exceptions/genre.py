from core.exceptions.base import ConflictError, NotFoundError


class GenreNotFoundError(NotFoundError):
    """
    Класс для ошибок, связанных с ненахождением жанра фильма.
    """

    def __init__(self, detail: str) -> None:
        super().__init__(detail)


class GenreIdNotFoundError(GenreNotFoundError):
    """
    Класс для ошибок, связанных с ненайденным id жанра фильма.
    """

    def __init__(self, genre_id: int) -> None:
        self.genre_id = genre_id
        detail = f"Genre with genre id = {genre_id} not found."
        super().__init__(detail)


class GenreNameAlreadyExistsError(ConflictError):
    """
    Класс для ошибок, связанных с уже существующим именем жанра фильма.
    """

    def __init__(self, genre_name: str) -> None:
        self.genre_name = genre_name
        detail = f"Genre with genre name = {genre_name} already exists."
        super().__init__(detail)


class GenreAlreadyHasMoviesError(ConflictError):
    """
    Класс для ошибок, связанных с уже существующими фильмами такого жанра.
    """

    def __init__(self, detail: str) -> None:
        super().__init__(detail)


class GenreIdAlreadyHasMoviesError(GenreAlreadyHasMoviesError):
    """
    Класс для ошибок, связанных с уже существующими фильмами такого id жанра.
    """

    def __init__(self, genre_id: int) -> None:
        self.genre_id = genre_id
        detail = f"Genre with genre id = {genre_id} has movies. Delete movies first."
        super().__init__(detail)
