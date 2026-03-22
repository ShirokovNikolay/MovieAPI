from datetime import datetime

from sqlalchemy import String, ForeignKey, CheckConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING
from database import Base

if TYPE_CHECKING:
    from models import User, Movie


class Review(Base):
    __tablename__ = "reviews"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship("User", back_populates="reviews")
    movie_id: Mapped[int] = mapped_column(ForeignKey("movies.id"))
    movie: Mapped["Movie"] = relationship("Movie", back_populates="reviews")
    review_text: Mapped[str | None] = mapped_column(String(400))
    rating: Mapped[int] = mapped_column(CheckConstraint("0 <= rating <= 10"))
    publication_date: Mapped[datetime] = mapped_column(server_default=func.now())
