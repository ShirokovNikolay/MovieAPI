from core.exceptions.base import AuthenticationError, ForbiddenError


class InvalidTokenError(AuthenticationError):
    """
    Класс для ошибок неправильного токена.
    """

    def __init__(self, detail: str):
        super().__init__(detail)


class InvalidJWTAccessTokenError(InvalidTokenError):
    """
    Класс для ошибок из-за невалидного access jwt-токена.
    """

    def __init__(self, token: str):
        self.invalid_access_token = token
        detail = f"Invalid JWT access token = {token}"
        super().__init__(detail)


class JWTAccessTokenExpiredError(InvalidTokenError):
    """
    Класс для ошибок из-за истекшего срока access jwt-токена.
    """

    def __init__(self, exp_time: str):
        self.exp_time = exp_time
        detail = f"JWT access token expired at {exp_time}"
        super().__init__(detail)


class InvalidJWTRefreshTokenError(InvalidTokenError):
    """
    Класс для ошибок из-за невалидного refresh jwt-токена.
    """

    def __init__(self, token: str):
        self.invalid_token = token
        detail = f"Invalid JWT refresh token = {token}"
        super().__init__(detail)


class JWTRefreshTokenExpiredError(InvalidTokenError):
    """
    Класс для ошибок из-за истекшего срока refresh jwt-токена.
    """

    def __init__(self, exp_time: str):
        self.exp_time = exp_time
        detail = f"JWT refresh token expired at {exp_time}"
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
