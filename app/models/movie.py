from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship
from database import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .genre import Genre


class Movie(Base):
    __tablename__ = "movies"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    description: Mapped[str | None]
    preview_url: Mapped[str]
    source_url: Mapped[str]
    genre_id: Mapped[int] = mapped_column(ForeignKey("genres.id"))
    genre: Mapped["Genre"] = relationship(back_populates="movies")
    release_date: Mapped[datetime]
