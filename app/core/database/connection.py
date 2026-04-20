from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
)
from sqlalchemy.orm import declarative_base, DeclarativeBase

from core.config import settings


# Base = declarative_base()
class Base(DeclarativeBase):
    """
    Базовый класс для работы с метаданными.
    """


engine = create_async_engine(
    url=settings.database.url_database,
    echo=settings.debug,
)

session_factory = async_sessionmaker(
    bind=engine,
)
