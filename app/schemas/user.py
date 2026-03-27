from datetime import datetime
from typing import Annotated

from annotated_types import MaxLen
from pydantic import BaseModel, ConfigDict

StringMaxLength255 = Annotated[
    str,
    MaxLen(max_length=255),
]

StringMaxLength30 = Annotated[
    str,
    MaxLen(max_length=30),
]

StringMaxLength20 = Annotated[
    str,
    MaxLen(max_length=20),
]


class UserBase(BaseModel):
    """
    Базовая модель для пользователя.
    """

    surname: StringMaxLength30
    name: StringMaxLength20
    login: StringMaxLength20
    email: StringMaxLength255
    model_config: ConfigDict = ConfigDict(from_attributes=True)


class UserCreate(UserBase):
    """
    Модель для создания пользователя.
    """

    password: StringMaxLength20


class UserUpdate(UserBase):
    """
    Модель для обновления данных о пользователе
    """

    password: StringMaxLength20


class UserPartialUpdate(UserBase):
    """
    Модель для частичного обновления данных о пользователе.
    """

    surname: StringMaxLength30 | None = None
    name: StringMaxLength20 | None = None
    login: StringMaxLength20 | None = None
    email: StringMaxLength255 | None = None
    password: StringMaxLength20 | None = None


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
    model_config: ConfigDict = ConfigDict(from_attributes=True)
