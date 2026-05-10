from datetime import datetime
from typing import ClassVar

from pydantic import BaseModel, ConfigDict

from schemas.movie import MovieResponse


class WatchHistoryBase(BaseModel):
    """
    Базовая модель для отображения просмотра фильма пользователем.
    """

    movie_id: int
    model_config: ClassVar[ConfigDict] = ConfigDict(from_attributes=True)


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


class WatchHistoryWithMovieResponse(WatchHistoryResponse):
    """
    Модель для вывода информации о просмотре фильма с подгрузкой данных о нем.
    """

    movie: MovieResponse


class WatchHistoryWithMovieResponseList(BaseModel):
    """
    Модель для вывода истории просмотров фильмов c подгрузкой данных о нем.
    """

    watch_history_list: list[WatchHistoryWithMovieResponse]
    size: int
    page: int
