from typing import Generator, Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from database import session_factory
from services import GenreService


def get_db() -> Generator:
    try:
        db = session_factory()
        yield db
    finally:
        db.close()


def get_genre_service(
    session: Annotated[Session, Depends(get_db)],
):
    try:
        genre_service = GenreService(session)
        yield genre_service
    finally:
        """
        Действия после view.
        """
