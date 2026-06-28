from datetime import date

from pydantic import BaseModel, EmailStr


class SendEmailRequest(BaseModel):
    """
    Модель для отправки сообщения на почту.
    """

    subject: str
    to_email: EmailStr
    body: str


class InactiveUser(BaseModel):
    """
    Модель для получения информации о неактивном пользователе.
    """

    name: str
    email: EmailStr


class InactiveUserList(BaseModel):
    """
    Модель для получения списка неактивных пользователей.
    """

    inactive_user_list: list[InactiveUser]


class SelectedMovie(BaseModel):
    """
    Модель для получения рекомендованного фильма.
    """

    name: str
    genre_name: str
    rating: int
    source_url: str
    release_date: date


class SelectedMovieList(BaseModel):
    """
    Модель для получения списка рекомендованных фильмов.
    """

    selected_movie_list: list[SelectedMovie]


class SendInactiveUsersMovieSelectionData(BaseModel):
    """
    Модель для получения неактивных пользователей и рекомендованных фильмов.
    """

    inactive_users: InactiveUserList
    movie_selection: SelectedMovieList
