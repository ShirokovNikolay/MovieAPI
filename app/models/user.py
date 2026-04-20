from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Enum, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.constants import UserRole
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
    surname: Mapped[str] = mapped_column(String(30))
    name: Mapped[str] = mapped_column(String(20))
    login: Mapped[str] = mapped_column(String(20))
    email: Mapped[str] = mapped_column(String(255))
    encrypted_password: Mapped[str] = mapped_column(String(128))
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
