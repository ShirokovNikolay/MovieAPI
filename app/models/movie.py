from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.constants import (
    MOVIE_DESCRIPTION_MAX_LENGTH,
    MOVIE_NAME_MAX_LENGTH,
    MOVIE_URL_MAX_LENGTH,
)
from core.database.connection import Base

if TYPE_CHECKING:
    from models import FavoriteMovie, Genre, Review, WatchHistory


class Movie(Base):
    __tablename__ = "movies"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(
        String(MOVIE_NAME_MAX_LENGTH),
        unique=True,
    )
    description: Mapped[str | None] = mapped_column(
        String(MOVIE_DESCRIPTION_MAX_LENGTH),
        nullable=True,
    )
    rating: Mapped[float]
    preview_url: Mapped[str] = mapped_column(String(MOVIE_URL_MAX_LENGTH))
    source_url: Mapped[str] = mapped_column(String(MOVIE_URL_MAX_LENGTH))
    genre_id: Mapped[int] = mapped_column(
        ForeignKey(
            "genres.id",
            name="fk_movies_genre_id",
        ),
    )
    release_date: Mapped[datetime]
    genre: Mapped["Genre"] = relationship(
        "Genre",
        back_populates="movies",
    )
    reviews: Mapped[list["Review"]] = relationship(
        "Review",
        back_populates="movie",
    )
    favorited_by_users: Mapped[list["FavoriteMovie"]] = relationship(
        "FavoriteMovie",
        back_populates="movie",
    )
    watch_history: Mapped[list["WatchHistory"]] = relationship(
        "WatchHistory",
        back_populates="movie",
    )

    __table_args__ = (
        UniqueConstraint("name", name="uq_movies_name"),
        CheckConstraint(
            "LENGTH(name) >= 3 AND LENGTH(name) <= 20",
            name="ch_movies_name",
        ),
        CheckConstraint(
            "rating >= 1 AND rating <= 10",
            name="ch_movies_rating",
        ),
    )
