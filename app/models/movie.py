from datetime import datetime

from sqlalchemy import ForeignKey, CheckConstraint
from sqlalchemy.orm import mapped_column, Mapped, relationship
from database.connection import Base
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from models import Genre, Review, FavoriteMovie, WatchHistory


class Movie(Base):
    __tablename__ = "movies"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    description: Mapped[str | None]
    rating: Mapped[float] = mapped_column(
        CheckConstraint(
            "0 <= rating <= 10",
            name="ck_movies_rating",
        )
    )
    preview_url: Mapped[str]
    source_url: Mapped[str]
    genre_id: Mapped[int] = mapped_column(
        ForeignKey(
            "genres.id",
            name="fk_movies_genre_id",
        )
    )
    genre: Mapped["Genre"] = relationship(
        "Genre",
        back_populates="movies",
    )
    release_date: Mapped[datetime]
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
