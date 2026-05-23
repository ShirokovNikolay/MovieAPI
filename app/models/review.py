from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.constants import REVIEW_TEXT_MAX_LENGTH
from core.database.connection import Base

if TYPE_CHECKING:
    from models import Movie, User


class Review(Base):
    __tablename__ = "reviews"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey(
            "users.id",
            name="fk_reviews_user_id",
            ondelete="CASCADE",
        ),
    )
    movie_id: Mapped[int] = mapped_column(
        ForeignKey(
            "movies.id",
            name="fk_reviews_movie_id",
            ondelete="CASCADE",
        ),
    )
    review_text: Mapped[str | None] = mapped_column(String(REVIEW_TEXT_MAX_LENGTH))
    rating: Mapped[int]
    publication_date: Mapped[datetime] = mapped_column(server_default=func.now())
    user: Mapped["User"] = relationship(
        "User",
        back_populates="reviews",
    )
    movie: Mapped["Movie"] = relationship(
        "Movie",
        back_populates="reviews",
    )
    __table_args__ = (
        CheckConstraint(
            "rating >= 1 AND rating <= 10",
            name="ch_reviews_rating",
        ),
    )
