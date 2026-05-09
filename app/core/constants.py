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


class UserRole(StrEnum):
    user = "user"
    admin = "admin"


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
# Genre
GENRE_NAME_MIN_LENGTH = 3
GENRE_NAME_MAX_LENGTH = 30
GENRE_DESCRIPTION_MAX_LENGTH = 200
# Movie
MOVIE_NAME_MIN_LENGTH = 3
MOVIE_NAME_MAX_LENGTH = 20
MOVIE_DESCRIPTION_MIN_LENGTH = 0
MOVIE_DESCRIPTION_MAX_LENGTH = 200
MOVIE_RATING_MIN_VALUE = 0
MOVIE_RATING_MAX_VALUE = 10
# Review
REVIEW_TEXT_MIN_LENGTH = 0
REVIEW_TEXT_MAX_LENGTH = 400
REVIEW_RATING_MIN_VALUE = 0
REVIEW_RATING_MAX_VALUE = 10
# User
USER_SURNAME_MIN_LENGTH = 3
USER_SURNAME_MAX_LENGTH = 30
USER_NAME_MIN_LENGTH = 3
USER_NAME_MAX_LENGTH = 20
USER_LOGIN_MIN_LENGTH = 3
USER_LOGIN_MAX_LENGTH = 20
USER_EMAIL_MIN_LENGTH = 10
USER_EMAIL_MAX_LENGTH = 40
USER_PASSWORD_MIN_LENGTH = 8
USER_PASSWORD_MAX_LENGTH = 30
USER_ENCRYPTED_PASSWORD_MAX_LENGTH = 128
