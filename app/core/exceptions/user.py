from core.exceptions.base import ConflictError, NotFoundError


class UserNotFoundError(NotFoundError):
    """
    Класс для ошибок, связанных с ненахождением пользователя.
    """

    def __init__(self, detail: str) -> None:
        super().__init__(detail)


class UserIdNotFoundError(NotFoundError):
    """
    Класс для ошибок, связанных с ненахождением пользователя с таким id.
    """

    def __init__(self, user_id: int) -> None:
        self.user_id = user_id
        detail = f"User with id = {user_id} not found."
        super().__init__(detail)


class UserLoginNotFoundError(NotFoundError):
    """
    Класс для ошибок, связанных с ненахождением пользователя с таким логином.
    """

    def __init__(self, login: str) -> None:
        detail = f"User with login = {login} not found."
        super().__init__(detail)


class UserEmailNotFoundError(NotFoundError):
    """
    Класс для ошибок, связанных с ненахождением пользователя с такой почтой.
    """

    def __init__(self, email: str) -> None:
        detail = f"User with email = {email} not found."
        super().__init__(detail)


class UserAlreadyExistsError(ConflictError):
    """
    Класс для ошибок, связанных с существованием пользователя
    с такой же уникальной характеристикой.
    """

    def __init__(self, detail: str) -> None:
        super().__init__(detail)


class UserLoginAlreadyExistsError(UserAlreadyExistsError):
    """
    Класс для ошибок, связанных с существованием пользователя с таким логином.
    """

    def __init__(self, login: str) -> None:
        detail = f"User with login = {login} already exists."
        super().__init__(detail)


class UserEmailAlreadyExistsError(UserAlreadyExistsError):
    """
    Класс для ошибок, связанных с существованием пользователя с такой почтой.
    """

    def __init__(self, email: str) -> None:
        detail = f"User with email = {email} already exists."
        super().__init__(detail)
