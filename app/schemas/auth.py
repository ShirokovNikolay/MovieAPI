from typing import Annotated

from annotated_types import Len
from pydantic import BaseModel, EmailStr

from schemas.user import LoginConstraint, PasswordConstraint

ConfirmationCode = Annotated[
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
    confirmation_code: ConfirmationCode
