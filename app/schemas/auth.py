from typing import Annotated

from annotated_types import Len
from pydantic import BaseModel, EmailStr

from schemas.user import LoginConstraint, PasswordConstraint

ConfirmationCodeConstraint = Annotated[
    str,
    Len(
        min_length=6,
        max_length=6,
    ),
]


class UserLogin(BaseModel):
    """
    Модель для аутентификации пользователя.
    """

    login: LoginConstraint
    password: PasswordConstraint


class SendConfirmationCodeRequest(BaseModel):
    """
    Модель для отправки кода подтверждения на почту.
    """

    token: str


class VerifyUserEmail(BaseModel):
    """
    Модель для подтверждения почты пользователя.
    """

    token: str
    confirmation_code: ConfirmationCodeConstraint


class ResetPasswordRequest(BaseModel):
    """
    Модель для смены пароля.
    """

    reset_password_token: str
    password: PasswordConstraint
    password_confirmation: PasswordConstraint


class RecoverAccountRequest(BaseModel):
    """
    Модель для восстановления доступа к аккаунту.
    """

    email: EmailStr
