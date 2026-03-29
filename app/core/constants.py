from enum import Enum

TOKEN_TYPE = "type"
ACCESS_TOKEN_TYPE = "access"
REFRESH_TOKEN_TYPE = "refresh"


class UserRole(str, Enum):
    user: str = "user"
    admin: str = "admin"
