from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload
from sqlalchemy import select, delete, and_, func, desc
from models import Movie, Genre
from schemas.movie import MovieCreate, MovieUpdate, MoviePartialUpdate


class MovieRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_movie_by_id(self, movie_id: int) -> Movie | None:
        stmt = (
            select(Movie)
            .options(
                joinedload(Movie.genre),
                selectinload(Movie.reviews),
                selectinload(Movie.favorited_by_users),
                selectinload(Movie.watch_history),
            )
            .where(Movie.id == movie_id)
        )

        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def get_movie_by_name(self, movie_name: str) -> Movie | None:
        stmt = select(Movie).where(Movie.name == movie_name)
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def movie_id_exists(self, movie_id: int) -> bool:
        return await self.get_movie_by_id(movie_id) is not None

    async def movie_name_exists(self, movie_name: str) -> bool:
        return await self.get_movie_by_name(movie_name) is not None

    async def get_movies(self) -> list[Movie]:
        stmt = select(Movie).options(joinedload(Movie.genre))
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def get_movies_by_genre_id(self, genre_id: int) -> list[Movie]:
        stmt = (
            select(Movie)
            .options(joinedload(Movie.genre))
            .where(Movie.genre_id == genre_id)
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def search_movies_by_name(self, name: str) -> list[Movie]:
        stmt = select(Movie).where(Movie.name.ilike("%" + name + "%"))
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def get_movies_by_rating_range(
        self, min_rating: int, max_rating: int
    ) -> list[Movie]:
        stmt = (
            select(Movie)
            .options(joinedload(Movie.genre))
            .where(
                Movie.rating.between(min_rating, max_rating),
            )
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def get_movies_by_year(self, year: int) -> list[Movie]:
        stmt = (
            select(Movie)
            .options(joinedload(Movie.genre))
            .where(
                func.extract("year", Movie.release_date) == year,
            )
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def get_movies_by_release_date(
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
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def get_top_rated_movies(self, limit: int) -> list[Movie]:
        stmt = (
            select(Movie)
            .options(joinedload(Movie.genre))
            .order_by(desc(Movie.rating))
            .limit(limit)
        )

        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def get_top_newest_movies(self, limit: int) -> list[Movie]:
        stmt = (
            select(Movie)
            .options(joinedload(Movie.genre))
            .order_by(desc(Movie.release_date))
            .limit(limit)
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def get_top_oldest_movies(self, limit: int) -> list[Movie]:
        stmt = (
            select(Movie)
            .options(joinedload(Movie.genre))
            .order_by(Movie.release_date)
            .limit(limit)
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def create_movie(self, create_movie_data: MovieCreate) -> Movie | None:
        movie = Movie(**create_movie_data.model_dump())
        self.session.add(movie)
        await self.session.commit()
        await self.session.refresh(movie)
        return movie

    async def update_movie(
        self,
        movie_id,
        update_movie_data: MovieUpdate,
    ) -> Movie | None:
        movie = await self.get_movie_by_id(movie_id)
        if movie is None:
            return None

        for field, value in update_movie_data.model_dump().items():
            setattr(movie, field, value)

        await self.session.commit()
        await self.session.refresh(movie)
        return movie

    async def partial_update_movie(
        self,
        movie_id,
        update_movie_data: MoviePartialUpdate,
    ) -> Movie | None:
        movie = await self.get_movie_by_id(movie_id)
        if movie is None:
            return None

        for field, value in update_movie_data.model_dump(exclude_unset=True).items():
            setattr(movie, field, value)

        await self.session.commit()
        await self.session.refresh(movie)
        return movie

    async def delete_movie_by_id(self, movie_id: int) -> bool:
        if await self.get_movie_by_id(movie_id) is None:
            return False

        stmt = delete(Movie).where(Movie.id == movie_id)
        await self.session.execute(stmt)
        await self.session.commit()
        return True
