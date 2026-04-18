from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.database.connection import Base


if TYPE_CHECKING:
    from models import User
    from models import Movie


class FavoriteMovie(Base):
    __tablename__ = "favorite_movies"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey(
            "users.id",
            name="fk_favorite_movies_user_id",
        ),
    )
    movie_id: Mapped[int] = mapped_column(
        ForeignKey(
            "movies.id",
            name="fk_favorite_movies_movie_id",
        ),
    )
    user: Mapped["User"] = relationship(
        "User",
        back_populates="favorite_movies",
    )
    movie: Mapped["Movie"] = relationship(
        "Movie",
        back_populates="favorited_by_users",
    )
