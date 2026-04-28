from pydantic import BaseModel

from schemas.user import LoginConstraint, PasswordConstraint


class UserLogin(BaseModel):
    """
    Модель для аутентификации пользователя.
    """

    login: LoginConstraint
    password: PasswordConstraint
