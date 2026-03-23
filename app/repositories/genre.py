from sqlalchemy.orm import Session
from sqlalchemy import select, delete

from models import Genre
from schemas.genre import GenreCreate, GenreUpdate, GenrePartialUpdate


class GenreRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def get_genre_by_id(self, genre_id: int) -> Genre | None:
        stmt = select(Genre).where(Genre.id == genre_id)
        return self.session.execute(stmt).scalars().first()

    def get_genre_by_name(self, name: str) -> Genre | None:
        stmt = select(Genre).where(Genre.name == name)
        return self.session.execute(stmt).scalars().first()

    def get_all_genres(self) -> list[Genre]:
        return list(self.session.execute(select(Genre)).scalars().all())

    def create_genre(self, create_data: GenreCreate) -> Genre:
        genre = Genre(**create_data.model_dump())
        self.session.add(genre)
        self.session.commit()
        self.session.refresh(genre)
        return genre

    def update_genre(
        self,
        genre_id: int,
        update_data: GenreUpdate,
    ) -> Genre | None:
        genre = self.get_genre_by_id(genre_id)
        if not genre:
            return None
        for field, value in update_data.model_dump():
            setattr(genre, field, value)

        self.session.commit()
        self.session.refresh(genre)
        return genre

    def partial_update_genre(
        self,
        genre_id: int,
        update_data: GenrePartialUpdate,
    ) -> Genre | None:
        genre = self.get_genre_by_id(genre_id)
        if not genre:
            return None

        for field, value in update_data.model_dump(exclude_unset=True):
            setattr(genre, field, value)

        self.session.commit()
        self.session.refresh(genre)
        return genre

    def delete_genre_by_id(self, genre_id: int) -> bool:
        if self.get_genre_by_id(genre_id) is None:
            return False
        stmt = delete(Genre).where(Genre.id == genre_id)
        self.session.execute(stmt)
        self.session.commit()
        return True

    def delete_genre_by_name(self, name: str) -> bool:
        if self.get_genre_by_name(name) is None:
            return False
        stmt = delete(Genre).where(Genre.name == name)
        self.session.execute(stmt)
        self.session.commit()
        return True
