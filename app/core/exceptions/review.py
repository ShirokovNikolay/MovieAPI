from core.exceptions.base import ConflictError, NotFoundError


class ReviewNotFoundError(NotFoundError):
    """
    Класс для ошибок, связанных с ненахождением отзыва.
    """

    def __init__(self, detail: str):
        super().__init__(detail)


class ReviewIdNotFoundError(ReviewNotFoundError):
    """
    Класс для ошибок, связанных с ненахождением id отзыва.
    """

    def __init__(self, review_id: int):
        self.review_id = review_id
        detail = f"Review with review id = {review_id} not found."
        super().__init__(detail)


class ReviewNotFoundByUserAndMovieError(ReviewNotFoundError):
    """
    Класс для ошибок, связанных с ненахождением отзыва пользователя по фильму.
    """

    def __init__(self, user_id: int, movie_id: int):
        self.user_id = user_id
        self.movie_id = movie_id
        detail = f"No review with owner user_id = {user_id} found for the movie with movie_id = {movie_id}."
        super().__init__(detail)


class ReviewAlreadyExistsError(ConflictError):
    """
    Класс для ошибок, связанных с уже существующим отзывом.
    """

    def __init__(self, detail: str):
        super().__init__(detail)


class ReviewAlreadyExistsByUserAndMovieError(ReviewAlreadyExistsError):
    """
    Класс для ошибок, связанных с существованием отзыва пользователя по фильму.
    """

    def __init__(self, user_id: int, movie_id: int):
        self.user_id = user_id
        self.movie_id = movie_id
        detail = f"Review with owner user_id = {user_id} and movie with movie_id = {movie_id} already exists."
        super().__init__(detail)
