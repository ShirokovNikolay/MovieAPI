from datetime import datetime
from typing import Annotated, ClassVar

from annotated_types import Len
from pydantic import BaseModel, ConfigDict, EmailStr

SurnameConstraint = Annotated[
    str,
    Len(min_length=3, max_length=30),
]

NameConstraint = Annotated[
    str,
    Len(min_length=3, max_length=20),
]

LoginConstraint = Annotated[
    str,
    Len(min_length=3, max_length=20),
]

EmailConstraint = Annotated[
    EmailStr,
    Len(min_length=10, max_length=40),
]

PasswordConstraint = Annotated[
    str,
    Len(min_length=8, max_length=30),
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
    Модель для обновления данных о пользователе
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
    registration_date: datetime


class UserResponseList(BaseModel):
    """
    Модель для вывода информации о списке пользователей.
    """

    user_list: list[UserResponse]
    size: int
    page: int
    model_config: ClassVar[ConfigDict] = ConfigDict(from_attributes=True)


class UserLogin(BaseModel):
    """
    Модель для аутентификации пользователя.
    """

    login: LoginConstraint
    password: PasswordConstraint
