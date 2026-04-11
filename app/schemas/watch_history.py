from datetime import datetime

from pydantic import BaseModel, ConfigDict


class WatchHistoryBase(BaseModel):
    """
    Базовая модель для отображения просмотра фильма пользователем.
    """

    movie_id: int
    model_config: ConfigDict = ConfigDict(from_attributes=True)


class WatchHistoryCreate(WatchHistoryBase):
    """
    Модель для создания записи о просмотре фильма пользователем.
    """


class WatchHistoryResponse(WatchHistoryBase):
    """
    Модель для вывода информации о просмотре фильма пользователем в истории.
    """

    id: int
    user_id: int
    watched_at: datetime


class WatchHistoryResponseList(BaseModel):
    """
    Модель для вывода истории просмотров фильмов пользователем.
    """

    watch_history_list: list[WatchHistoryResponse]
    size: int
    page: int
