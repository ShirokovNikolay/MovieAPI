from typing import Annotated

from annotated_types import Len
from pydantic import BaseModel, EmailStr

from core.constants import MessageType
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


class ConfirmEmailRequest(BaseModel):
    """
    Модель для двухфакторной аутентификации:
    подтверждение через дополнительный код.
    """

    email: EmailStr
    confirmation_code: ConfirmationCodeConstraint


class SendAuthEmail(BaseModel):
    """
    Модель для отправки писем, связанных с аутентификацией, на почту.
    """

    email: EmailStr
    message_type: MessageType


class ResetPasswordRequest(BaseModel):
    """
    Модель для смены пароля.
    """

    email: EmailStr
    password: PasswordConstraint
    password_confirmation: PasswordConstraint
    confirmation_code: ConfirmationCodeConstraint
