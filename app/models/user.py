from datetime import datetime

from sqlalchemy import String, func
from sqlalchemy.orm import mapped_column, Mapped

from database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        primary_key=True,
    )
    surname: Mapped[str] = mapped_column(String(30))
    name: Mapped[str] = mapped_column(String(20))
    login: Mapped[str] = mapped_column(String(20))
    encrypted_password: Mapped[str] = mapped_column(String(20))
    registration_date: Mapped[datetime] = mapped_column(
        String(20), server_default=func.now()
    )
