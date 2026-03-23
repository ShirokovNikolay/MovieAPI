from datetime import datetime

from sqlalchemy.orm import Session, joinedload
from sqlalchemy import select, delete, and_, func, between, desc
from models import Movie
from schemas.movie import MovieCreate, MovieUpdate, MoviePartialUpdate


class MovieRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_movie_by_id(self, movie_id: int) -> Movie | None:
        stmt = (
            select(Movie).options(joinedload(Movie.genre)).where(Movie.id == movie_id)
        )
        return self.session.execute(stmt).scalars().first()

    def get_movie_by_name(self, movie_name: str) -> Movie | None:
        stmt = select(Movie).where(Movie.name == movie_name)
        return self.session.execute(stmt).scalars().first()

    def get_movies_by_genre_id(self, genre_id: int) -> list[Movie]:
        stmt = (
            select(Movie)
            .options(joinedload(Movie.genre))
            .where(Movie.genre_id == genre_id)
        )
        return list(self.session.execute(stmt).scalars().all())

    def get_movies_by_rating_range(
        self, min_rating: int, max_rating: int
    ) -> list[Movie]:
        stmt = (
            select(Movie)
            .options(joinedload(Movie.genre))
            .where(
                Movie.rating.between(min_rating, max_rating),
            )
        )
        return list(self.session.execute(stmt).scalars().all())

    def get_movies_by_year(self, year: int) -> list[Movie]:
        stmt = (
            select(Movie)
            .options(joinedload(Movie.genre))
            .where(
                func.extract("year", Movie.release_date) == year,
            )
        )
        return list(self.session.execute(stmt).scalars().all())

    def get_movies_by_release_date(
        self,
        release_date_start: datetime,
        release_date_end: datetime,
    ) -> list[Movie]:
        stmt = (
            select(Movie)
            .options(joinedload(Movie.genre))
            .where(
                and_(
                    release_date_start <= Movie.release_date,
                    Movie.release_date <= release_date_end,
                )
            )
        )
        return list(self.session.execute(stmt).scalars().all())

    def get_top_rated_movies(self, limit: int) -> list[Movie]:
        stmt = (
            select(Movie)
            .options(joinedload(Movie.genre))
            .order_by(desc(Movie.rating))
            .limit(limit)
        )

        return list(self.session.execute(stmt).scalars().all())

    def get_top_newest_movies(self, limit: int) -> list[Movie]:
        stmt = (
            select(Movie)
            .options(joinedload(Movie.genre))
            .order_by(desc(Movie.release_date))
            .limit(limit)
        )
        return list(self.session.execute(stmt).scalars().all())

    def get_top_oldest_movies(self, limit: int) -> list[Movie]:
        stmt = (
            select(Movie)
            .options(joinedload(Movie.genre))
            .order_by(Movie.release_date)
            .limit(limit)
        )
        return list(self.session.execute(stmt).scalars().all())

    def create_movie(self, create_movie_data: MovieCreate) -> Movie | None:
        movie = Movie(**create_movie_data.model_dump())
        self.session.add(movie)
        self.session.commit()
        self.session.refresh(movie)
        return movie

    def update_movie(
        self,
        movie_id,
        update_movie_data: MovieUpdate,
    ) -> Movie | None:
        movie = self.get_movie_by_id(movie_id)
        if movie is None:
            return None

        for field, value in update_movie_data.model_dump():
            setattr(movie, field, value)

        self.session.commit()
        self.session.refresh(movie)
        return movie

    def partial_update_movie(
        self,
        movie_id,
        update_movie_data: MoviePartialUpdate,
    ) -> Movie | None:
        movie = self.get_movie_by_id(movie_id)
        if movie is None:
            return None

        for field, value in update_movie_data.model_dump(exclude_unset=True):
            setattr(movie, field, value)

        self.session.commit()
        self.session.refresh(movie)
        return movie

    def delete_movie_by_id(self, movie_id: int) -> bool:
        if self.get_movie_by_id(movie_id) is None:
            return False

        stmt = delete(Movie).where(Movie.id == movie_id)
        self.session.execute(stmt)
        self.session.commit()
        return True
