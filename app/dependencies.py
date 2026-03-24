from typing import Generator

from database import session_factory


def get_db() -> Generator:
    try:
        db = session_factory()
        yield db
    finally:
        db.close()
