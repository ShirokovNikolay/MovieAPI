from core.exceptions.base import AuthenticationError, ForbiddenError


class InvalidTokenError(AuthenticationError):
    """
    Класс для ошибок неправильного токена.
    """

    def __init__(self, detail: str):
        super().__init__(detail)


class InvalidJWTTokenError(InvalidTokenError):
    """
    Класс для ошибок из-за невалидного jwt-токена.
    """

    def __init__(self, token: str):
        self.invalid_token = token
        detail = f"Invalid JWT token = {token}"
        super().__init__(detail)


class JWTTokenExpiredError(InvalidTokenError):
    """
    Класс для ошибок из-за истекшего срока wt-токена.
    """

    def __init__(self, exp_time: str):
        self.exp_time = exp_time
        detail = f"JWT token expired at {exp_time}"
        super().__init__(detail)


class InvalidPasswordError(AuthenticationError):
    """
    Класс для ошибок, связанных с неправильным паролем.
    """

    def __init__(self):
        super().__init__("Invalid password")


class PermissionDeniedError(ForbiddenError):
    """
    Класс для ошибок, связанных с нехваткой прав доступа.
    """

    def __init__(self):
        super().__init__("You do not have access rights to use this resource.")
