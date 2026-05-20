from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, String, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.constants import (
    GENRE_DESCRIPTION_MAX_LENGTH,
    GENRE_NAME_MAX_LENGTH,
    GENRE_URL_MAX_LENGTH,
)
from core.database.connection import Base

if TYPE_CHECKING:
    from models import Movie


class Genre(Base):
    __tablename__ = "genres"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(GENRE_NAME_MAX_LENGTH))
    description: Mapped[str] = mapped_column(String(GENRE_DESCRIPTION_MAX_LENGTH))
    preview_url: Mapped[str] = mapped_column(String(GENRE_URL_MAX_LENGTH))
    movies: Mapped[list["Movie"]] = relationship(
        "Movie",
        back_populates="genre",
    )
    create_date: Mapped[datetime] = mapped_column(server_default=func.now())

    __table_args__ = (
        UniqueConstraint("name", name="uq_genres_name"),
        CheckConstraint(
            "LENGTH(name) >= 3 AND LENGTH(name) <= 30",
            name="ch_genres_name",
        ),
    )
