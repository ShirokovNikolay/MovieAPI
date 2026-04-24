from enum import StrEnum

from core.exceptions.base import (
    AuthenticationError,
    ConflictError,
    ForbiddenError,
    NotFoundError,
    TooManyRequestsError,
)
from core.exceptions.favorite_movie import (
    FavoriteMovieNotFoundError,
    FavoriteMovieAlreadyExistsError,
)
from core.exceptions.genre import (
    GenreNotFoundError,
    GenreAlreadyExistsError,
    GenreAlreadyHasMoviesError,
)
from core.exceptions.movie import MovieNotFoundError, MovieAlreadyExistsError

TOKEN_TYPE: str = "type"
ACCESS_TOKEN_TYPE: str = "access"
REFRESH_TOKEN_TYPE: str = "refresh"
BEARER_TOKEN_TYPE: str = "Bearer"

BASE_ERROR = (
    NotFoundError
    | ConflictError
    | ForbiddenError
    | AuthenticationError
    | TooManyRequestsError
)

BASE_GENRE_ERROR = (
    GenreNotFoundError | GenreAlreadyExistsError | GenreAlreadyHasMoviesError
)

BASE_MOVIE_ERROR = MovieNotFoundError | MovieAlreadyExistsError

BASE_FAVORITE_MOVIE_ERROR = FavoriteMovieNotFoundError | FavoriteMovieAlreadyExistsError


class UserRole(StrEnum):
    user = "user"
    admin = "admin"
