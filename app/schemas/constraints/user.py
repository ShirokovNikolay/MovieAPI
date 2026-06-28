from typing import Annotated

from annotated_types import Len
from pydantic import EmailStr

from core.constants import (
    USER_EMAIL_MAX_LENGTH,
    USER_EMAIL_MIN_LENGTH,
    USER_ENCRYPTED_PASSWORD_MAX_LENGTH,
    USER_LOGIN_MAX_LENGTH,
    USER_LOGIN_MIN_LENGTH,
    USER_NAME_MAX_LENGTH,
    USER_NAME_MIN_LENGTH,
    USER_PASSWORD_MAX_LENGTH,
    USER_PASSWORD_MIN_LENGTH,
    USER_SURNAME_MAX_LENGTH,
    USER_SURNAME_MIN_LENGTH,
)

SurnameConstraint = Annotated[
    str,
    Len(
        min_length=USER_SURNAME_MIN_LENGTH,
        max_length=USER_SURNAME_MAX_LENGTH,
    ),
]
NameConstraint = Annotated[
    str,
    Len(
        min_length=USER_NAME_MIN_LENGTH,
        max_length=USER_NAME_MAX_LENGTH,
    ),
]
LoginConstraint = Annotated[
    str,
    Len(
        min_length=USER_LOGIN_MIN_LENGTH,
        max_length=USER_LOGIN_MAX_LENGTH,
    ),
]
EmailConstraint = Annotated[
    EmailStr,
    Len(
        min_length=USER_EMAIL_MIN_LENGTH,
        max_length=USER_EMAIL_MAX_LENGTH,
    ),
]
PasswordConstraint = Annotated[
    str,
    Len(
        min_length=USER_PASSWORD_MIN_LENGTH,
        max_length=USER_PASSWORD_MAX_LENGTH,
    ),
]
EncryptedPasswordConstraint = Annotated[
    str,
    Len(
        max_length=USER_ENCRYPTED_PASSWORD_MAX_LENGTH,
    ),
]
