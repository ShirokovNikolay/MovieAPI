from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from core.config import settings

engine = create_engine(
    url=settings.database.url_database,
    echo=settings.debug,
)

session_factory = sessionmaker(
    bind=engine,
)

Base = declarative_base()
