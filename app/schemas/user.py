from datetime import datetime
from typing import Annotated, ClassVar

from annotated_types import Len
from pydantic import BaseModel, ConfigDict, EmailStr

from core.constants import (
    USER_EMAIL_MAX_LENGTH,
    USER_EMAIL_MIN_LENGTH,
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


class UserBase(BaseModel):
    """
    Базовая модель для пользователя.
    """

    surname: SurnameConstraint
    name: NameConstraint
    login: LoginConstraint
    email: EmailConstraint
    model_config: ClassVar[ConfigDict] = ConfigDict(from_attributes=True)


class UserCreate(UserBase):
    """
    Модель для создания пользователя.
    """

    password: PasswordConstraint


class UserUpdate(UserBase):
    """
    Модель для обновления данных о пользователе.
    """

    password: PasswordConstraint


class UserPartialUpdate(BaseModel):
    """
    Модель для частичного обновления данных о пользователе.
    """

    surname: SurnameConstraint | None = None
    name: NameConstraint | None = None
    login: LoginConstraint | None = None
    email: EmailConstraint | None = None
    password: PasswordConstraint | None = None


class UserResponse(UserBase):
    """
    Модель для вывода информации о пользователе.
    """

    id: int
    role: str
    registration_date: datetime


class UserResponseList(BaseModel):
    """
    Модель для вывода информации о списке пользователей.
    """

    user_list: list[UserResponse]
    size: int
    page: int
