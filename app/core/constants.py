from enum import StrEnum
from typing import TypeVar

from pydantic import BaseModel

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

BASE_MINIO_URL = "http://localhost:9000"

AnyPydanticType = TypeVar("AnyPydanticType", bound=BaseModel)

PrimitiveType = int | str | bool


class UserRole(StrEnum):
    user = "user"
    admin = "admin"


class SortType(StrEnum):
    date = "date"
    rating = "rating"


class SortMonotony(StrEnum):
    ascending = "ASC"
    descending = "DESC"


class MethodType(StrEnum):
    get = "GET"
    post = "POST"
    put = "PUT"
    patch = "PATCH"
    delete = "DELETE"


TOKEN_TYPE_FIELD = "type"
LOGIN_FIELD = "login"
EMAIL_FIELD = "email"

ACCESS_TOKEN_TYPE = "access"
REFRESH_TOKEN_TYPE = "refresh"
REGISTRATION_TOKEN_TYPE = "registration"
TWO_FACTOR_TOKEN_TYPE = "two_factor"
RECOVER_TOKEN_TYPE = "recover"
RESET_PASSWORD_TOKEN_TYPE = "reset_password"

BEARER_TOKEN_TYPE = "Bearer"

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
GENRE_NAME_MAX_LENGTH = 40
GENRE_DESCRIPTION_MIN_LENGTH = 0
GENRE_DESCRIPTION_MAX_LENGTH = 900
GENRE_URL_MAX_LENGTH = 255
# Movie
MOVIE_NAME_MIN_LENGTH = 3
MOVIE_NAME_MAX_LENGTH = 255
MOVIE_DESCRIPTION_MIN_LENGTH = 0
MOVIE_DESCRIPTION_MAX_LENGTH = 2000
MOVIE_RATING_MIN_VALUE = 1
MOVIE_RATING_MAX_VALUE = 10
MOVIE_URL_MAX_LENGTH = 255
# Review
REVIEW_TEXT_MIN_LENGTH = 0
REVIEW_TEXT_MAX_LENGTH = 2000
REVIEW_RATING_MIN_VALUE = 1
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
