from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from config import settings

engine = create_engine(
    url=settings.database.url_database,
    echo=settings.debug,
)

session_factory = sessionmaker(
    bind=engine,
)

base = declarative_base()


def init_db():
    base.metadata.create_all(
        bind=engine,
    )


def get_db():
    try:
        db = session_factory()
        yield db
    finally:
        db.close()
