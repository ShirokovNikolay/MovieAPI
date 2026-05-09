from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, Enum, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.constants import (
    USER_EMAIL_MAX_LENGTH,
    USER_ENCRYPTED_PASSWORD_MAX_LENGTH,
    USER_LOGIN_MAX_LENGTH,
    USER_NAME_MAX_LENGTH,
    USER_SURNAME_MAX_LENGTH,
    UserRole,
)
from core.database.connection import Base

if TYPE_CHECKING:
    from models import FavoriteMovie, Review, WatchHistory


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        primary_key=True,
    )
    role: Mapped[UserRole] = mapped_column(
        Enum(UserRole, name="user_role"),
        server_default=UserRole.user.value,
    )
    surname: Mapped[str] = mapped_column(String(USER_SURNAME_MAX_LENGTH))
    name: Mapped[str] = mapped_column(String(USER_NAME_MAX_LENGTH))
    login: Mapped[str] = mapped_column(String(USER_LOGIN_MAX_LENGTH))
    email: Mapped[str] = mapped_column(String(USER_EMAIL_MAX_LENGTH))
    encrypted_password: Mapped[str] = mapped_column(
        String(USER_ENCRYPTED_PASSWORD_MAX_LENGTH),
    )
    registration_date: Mapped[datetime] = mapped_column(server_default=func.now())
    reviews: Mapped[list["Review"]] = relationship(
        "Review",
        back_populates="user",
    )
    favorite_movies: Mapped[list["FavoriteMovie"]] = relationship(
        "FavoriteMovie",
        back_populates="user",
    )
    watch_history: Mapped[list["WatchHistory"]] = relationship(
        "WatchHistory",
        back_populates="user",
    )

    __table_args__ = (
        CheckConstraint(
            "LENGTH(surname) >= 3 AND LENGTH(surname) <= 30",
            name="ch_users_surname",
        ),
        CheckConstraint(
            "LENGTH(name) >= 3 AND LENGTH(name) <= 20",
            name="ch_users_name",
        ),
        CheckConstraint(
            "LENGTH(login) >= 3 AND LENGTH(login) <= 20",
            name="ch_users_login",
        ),
        CheckConstraint(
            "LENGTH(email) >= 10 AND LENGTH(email) <= 40",
            name="ch_users_email",
        ),
    )
