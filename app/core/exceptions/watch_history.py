from core.exceptions.base import NotFoundError


class WatchHistoryNotFoundError(NotFoundError):
    """
    Класс для ошибок, связанных с ненахождением записи в истории просмотров.
    """

    def __init__(self, detail: str) -> None:
        super().__init__(detail)


class WatchHistoryIdNotFoundError(WatchHistoryNotFoundError):
    """
    Класс для ошибок, связанных с ненахождением id записи в истории просмотров.
    """

    def __init__(self, watch_history_id: int) -> None:
        self.watch_history_id = watch_history_id
        detail = f"Watch history with watch history id = {watch_history_id} not found."
        super().__init__(detail)
