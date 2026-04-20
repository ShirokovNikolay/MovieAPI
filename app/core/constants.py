from enum import StrEnum

TOKEN_TYPE: str = "type"
ACCESS_TOKEN_TYPE: str = "access"
REFRESH_TOKEN_TYPE: str = "refresh"
BEARER_TOKEN_TYPE: str = "Bearer"


class UserRole(StrEnum):
    user = "user"
    admin = "admin"
