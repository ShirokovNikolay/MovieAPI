from sqlalchemy.ext.asyncio import (
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase

from core.config import settings


class Base(DeclarativeBase):
    """
    Базовый класс для работы с метаданными.
    """


engine = create_async_engine(
    url=settings.database.url,
    echo=settings.database.echo,
)

session_factory = async_sessionmaker(
    bind=engine,
)
