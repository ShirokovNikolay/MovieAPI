from enum import StrEnum

from core.exceptions.auth import (
    InvalidPasswordError,
    InvalidTokenError,
    PermissionDeniedError,
)
from core.exceptions.base import (
    AuthenticationError,
    ConflictError,
    ForbiddenError,
    NotFoundError,
    TooManyRequestsError,
)
from core.exceptions.favorite_movie import (
    FavoriteMovieAlreadyExistsError,
    FavoriteMovieNotFoundError,
)
from core.exceptions.genre import (
    GenreAlreadyExistsError,
    GenreAlreadyHasMoviesError,
    GenreNotFoundError,
)
from core.exceptions.movie import MovieAlreadyExistsError, MovieNotFoundError
from core.exceptions.review import ReviewAlreadyExistsError, ReviewNotFoundError
from core.exceptions.user import UserAlreadyExistsError, UserNotFoundError
from core.exceptions.watch_history import WatchHistoryNotFoundError

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

BASE_WATCH_HISTORY_ERROR = WatchHistoryNotFoundError

BASE_USER_ERROR = UserNotFoundError | UserAlreadyExistsError

BASE_REVIEW_ERROR = ReviewNotFoundError | ReviewAlreadyExistsError

BASE_AUTH_ERROR = InvalidTokenError | InvalidPasswordError | PermissionDeniedError


class UserRole(StrEnum):
    user = "user"
    admin = "admin"
