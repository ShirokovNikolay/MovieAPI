from core.exceptions.base import NotFoundError


class WatchHistoryNotFoundError(NotFoundError):
    """
    Класс для ошибок, связанных с ненахождением записи в истории просмотров.
    """

    def __init__(self, detail: str):
        super().__init__(detail)


class WatchHistoryIdNotFoundError(NotFoundError):
    """
    Класс для ошибок, связанных с ненахождением id записи в истории просмотров.
    """

    def __init__(self, watch_history_id: int):
        detail = f"Watch history with watch history id = {watch_history_id} not found."
        super().__init__(detail)
