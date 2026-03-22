from datetime import datetime

from sqlalchemy.orm import mapped_column, Mapped
from database import Base


class Movie(Base):
    __tablename__ = "movies"
    id: Mapped[int] = mapped_column(
        primary_key=True,
    )
    name: Mapped[str]
    description: Mapped[str]
    release_date: Mapped[datetime]
