from datetime import datetime

from sqlalchemy import String, func, Enum
from sqlalchemy.orm import mapped_column, Mapped, relationship

from core.constants import UserRole
from database import Base

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models import Review


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        primary_key=True,
    )
    role: Mapped[UserRole] = mapped_column(
        Enum(UserRole, name="user_role"),
        server_default=UserRole.user.value,
    )
    surname: Mapped[str] = mapped_column(String(30))
    name: Mapped[str] = mapped_column(String(20))
    login: Mapped[str] = mapped_column(String(20))
    email: Mapped[str] = mapped_column(String(255))
    encrypted_password: Mapped[str] = mapped_column(String(128))
    registration_date: Mapped[datetime] = mapped_column(server_default=func.now())
    reviews: Mapped[list["Review"]] = relationship(
        "Review",
        back_populates="user",
    )
