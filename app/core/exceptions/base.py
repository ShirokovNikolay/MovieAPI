class NotFoundError(Exception):
    """
    Базовый класс для ошибок, связанных с ненайденными объектами.
    """

    def __init__(self, detail: str) -> None:
        self.detail = detail
        super().__init__(detail)


class ConflictError(Exception):
    """
    Базовый класс для конфликтных ошибок.
    """

    def __init__(self, detail: str) -> None:
        self.detail = detail
        super().__init__(detail)


class ForbiddenError(Exception):
    """
    Базовый класс для ошибок авторизации.
    """

    def __init__(self, detail: str) -> None:
        self.detail = detail
        super().__init__(detail)


class AuthenticationError(Exception):
    """
    Базовый класс для ошибок аутентификации.
    """

    def __init__(self, detail: str) -> None:
        self.detail = detail
        super().__init__(detail)


class TooManyRequestsError(Exception):
    """
    Базовый класс для ошибок, связанных со слишком частыми запросами.
    """

    def __init__(self, detail: str) -> None:
        self.detail = detail
        super().__init__(detail)
