from enum import StrEnum

from core.exceptions.base import (
    AuthenticationError,
    ConflictError,
    ForbiddenError,
    NotFoundError,
    TooManyRequestsError,
)
from core.exceptions.genre import (
    GenreNotFoundError,
    GenreAlreadyExistsError,
    GenreAlreadyHasMoviesError,
)

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


class UserRole(StrEnum):
    user = "user"
    admin = "admin"
