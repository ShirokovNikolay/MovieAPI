from datetime import datetime
from typing import ClassVar

from pydantic import BaseModel, ConfigDict

from schemas.constraints.user import (
    EmailConstraint,
    EncryptedPasswordConstraint,
    LoginConstraint,
    NameConstraint,
    PasswordConstraint,
    SurnameConstraint,
)


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

    encrypted_password: EncryptedPasswordConstraint


class UserRegistration(UserBase):
    """
    Модель для регистрирования пользователя.
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
    size: int | None = None
    page: int | None = None
