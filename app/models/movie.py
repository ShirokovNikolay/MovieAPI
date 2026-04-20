from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.database.connection import Base

if TYPE_CHECKING:
    from models import FavoriteMovie, Genre, Review, WatchHistory


class Movie(Base):
    __tablename__ = "movies"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    description: Mapped[str | None]
    rating: Mapped[float] = mapped_column(
        CheckConstraint(
            "0 <= rating <= 10",
            name="ck_movies_rating",
        ),
    )
    preview_url: Mapped[str]
    source_url: Mapped[str]
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
