from datetime import datetime

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import mapped_column, Mapped, relationship

from database.connection import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models import User
    from models import Movie


class WatchHistory(Base):
    __tablename__ = "watch_history"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey(
            "users.id",
            name="fk_watch_history_user_id",
        )
    )
    movie_id: Mapped[int] = mapped_column(
        ForeignKey(
            "movies.id",
            name="fk_watch_history_movie_id",
        )
    )
    watched_at: Mapped[datetime] = mapped_column(server_default=func.now())
    user: Mapped["User"] = relationship(
        "User",
        back_populates="watch_history",
    )
    movie: Mapped["Movie"] = relationship(
        "Movie",
        back_populates="watch_history",
    )
