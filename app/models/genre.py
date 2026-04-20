from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.database.connection import Base

if TYPE_CHECKING:
    from models import Movie


class Genre(Base):
    __tablename__ = "genres"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(20))
    description: Mapped[str] = mapped_column(String(200))
    movies: Mapped[list["Movie"]] = relationship(
        "Movie",
        back_populates="genre",
    )
    create_date: Mapped[datetime] = mapped_column(server_default=func.now())
