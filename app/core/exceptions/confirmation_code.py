from pydantic import EmailStr

from core.exceptions.base import AuthenticationError, NotFoundError


class ConfirmationCodeNotFoundError(NotFoundError):
    """
    Класс для ошибок, связанных с ненахождением кода подтверждения.
    """

    def __init__(self, detail: str) -> None:
        super().__init__(detail)


class EmailConfirmationCodeNotFoundError(ConfirmationCodeNotFoundError):
    """
    Класс для ошибок, связанных с ненахождением кода подтверждения на почте.
    """

    def __init__(self, email: EmailStr) -> None:
        self.email = email
        detail = f"The active confirmation code for email {email} does not exist."
        super().__init__(detail)


class InvalidConfirmationCodeError(AuthenticationError):
    """
    Класс для ошибок, связанных с вводом некорректного кода подтверждения.
    """

    def __init__(self, detail: str) -> None:
        super().__init__(detail)


class InvalidEmailConfirmationCodeError(InvalidConfirmationCodeError):
    """
    Класс для ошибок, связанных с некорректным кодом подтверждения,
    отправленным на почту.
    """

    def __init__(self, email: EmailStr, confirmation_code: str) -> None:
        self.email = email
        self.confirmation_code = confirmation_code
        detail = (
            f"The confirmation code {confirmation_code} for email {email} is not valid."
        )
        super().__init__(detail)
