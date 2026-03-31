from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base

from core.config import settings

engine = create_async_engine(
    url=settings.database.url_database,
    echo=settings.debug,
)

session_factory = async_sessionmaker(
    bind=engine,
)

Base = declarative_base()
