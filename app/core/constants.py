from enum import StrEnum

from core.exceptions.base import (
    AuthenticationError,
    ConflictError,
    ForbiddenError,
    NotFoundError,
    TooManyRequestsError,
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


class UserRole(StrEnum):
    user = "user"
    admin = "admin"
