from core.exceptions.base import NotFoundError, ConflictError


class UserNotFoundError(NotFoundError):
    """
    Класс для ошибок, связанных с ненахождением пользователя.
    """

    def __init__(self, detail: str):
        super().__init__(detail)


class UserLoginNotFoundError(NotFoundError):
    """
    Класс для ошибок, связанных с ненахождением пользователя с таким логином.
    """

    def __init__(self, login: str):
        detail = f"User with login name = {login} not found."
        super().__init__(detail)


class UserEmailNotFoundError(NotFoundError):
    """
    Класс для ошибок, связанных с ненахождением пользователя с такой почтой.
    """

    def __init__(self, email: str):
        detail = f"User with email = {email} not found."
        super().__init__(detail)


class UserAlreadyExistsError(ConflictError):
    """
    Класс для ошибок, связанных с существованием пользователя
    с такой же уникальной характеристикой.
    """

    def __init__(self, detail: str):
        super().__init__(detail)


class UserLoginAlreadyExistsError(UserAlreadyExistsError):
    """
    Класс для ошибок, связанных с существованием пользователя с таким логином.
    """

    def __init__(self, login: str):
        detail = f"User with login = {login} already exists."
        super().__init__(detail)


class UserEmailAlreadyExistsError(UserAlreadyExistsError):
    """
    Класс для ошибок, связанных с существованием пользователя с такой почтой.
    """

    def __init__(self, email: str):
        detail = f"User with email = {email} already exists."
        super().__init__(detail)
