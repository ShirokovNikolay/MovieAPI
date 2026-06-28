from pydantic import BaseModel, EmailStr

from schemas.constraints.auth import ConfirmationCodeConstraint
from schemas.constraints.user import LoginConstraint, PasswordConstraint


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


class RecoverAccountRequest(BaseModel):
    """
    Модель для получения токена для восстановления доступа к аккаунту.
    """

    email: EmailStr


class ResetPasswordRequest(BaseModel):
    """
    Модель для смены пароля по токену.
    """

    reset_password_token: str
    password: PasswordConstraint
    password_confirmation: PasswordConstraint
