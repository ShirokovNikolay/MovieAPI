from enum import Enum

TOKEN_TYPE: str = "type"
ACCESS_TOKEN_TYPE: str = "access"
REFRESH_TOKEN_TYPE: str = "refresh"


class UserRole(str, Enum):
    user = "user"
    admin = "admin"
