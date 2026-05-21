from sqlalchemy import Date, cast, delete, desc, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from core.constants import SortMonotony, SortType
from dependencies.annotations.validators import PaginationPageDep, PaginationSizeDep
from models import Movie
from schemas.movie import MovieCreate, MovieFilter, MoviePartialUpdate, MovieUpdate


class MovieRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_movie_by_id(self, movie_id: int) -> Movie | None:
        stmt = (
            select(Movie)
            .options(
                joinedload(Movie.genre),
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

    async def get_movies(
        self,
        size: int = 10,
        page: int = 1,
    ) -> list[Movie]:
        stmt = (
            select(Movie)
            .options(joinedload(Movie.genre))
            .limit(size)
            .offset(size * (page - 1))
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def search_movies_with_filters(  # noqa: C901
        self,
        movie_filter: MovieFilter,
        size: PaginationSizeDep = 10,
        page: PaginationPageDep = 1,
    ) -> list[Movie]:
        stmt = select(Movie).options(joinedload(Movie.genre))
        if movie_filter.genre_id is not None:
            stmt = stmt.where(Movie.genre_id == movie_filter.genre_id)

        if movie_filter.min_rating is not None:
            stmt = stmt.where(Movie.rating >= movie_filter.min_rating)

        if movie_filter.max_rating is not None:
            stmt = stmt.where(Movie.rating <= movie_filter.max_rating)

        if movie_filter.start_release_date is not None:
            stmt = stmt.where(
                cast(Movie.release_date, Date) >= movie_filter.start_release_date,
            )

        if movie_filter.end_release_date is not None:
            stmt = stmt.where(
                cast(Movie.release_date, Date) <= movie_filter.end_release_date,
            )

        if movie_filter.search_query is not None:
            stmt = stmt.where(Movie.name.ilike("%" + movie_filter.search_query + "%"))

        if movie_filter.sort_by == SortType.date.value:
            if movie_filter.sorting_direction == SortMonotony.ascending.value:
                stmt = stmt.order_by(Movie.release_date)
            else:
                stmt = stmt.order_by(desc(Movie.release_date))

        if movie_filter.sort_by == SortType.rating.value:
            if movie_filter.sorting_direction == SortMonotony.ascending.value:
                stmt = stmt.order_by(Movie.rating)
            else:
                stmt = stmt.order_by(desc(Movie.rating))

        stmt = stmt.offset(size * (page - 1)).limit(size)
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def get_movies_by_genre_id(
        self,
        genre_id: int,
        size: int = 10,
        page: int = 1,
    ) -> list[Movie]:
        stmt = (
            select(Movie)
            .where(Movie.genre_id == genre_id)
            .limit(size)
            .offset(size * (page - 1))
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def create_movie(self, create_movie_data: MovieCreate) -> Movie | None:
        movie = Movie(**create_movie_data.model_dump())
        self.session.add(movie)
        await self.session.commit()
        await self.session.refresh(movie)
        return await self.get_movie_by_id(movie.id)

    async def update_movie(
        self,
        movie_id: int,
        update_movie_data: MovieUpdate,
    ) -> Movie | None:
        movie = await self.get_movie_by_id(movie_id)
        if movie is None:
            return None

        for field, value in update_movie_data.model_dump().items():
            setattr(movie, field, value)

        await self.session.commit()
        await self.session.refresh(movie)
        return await self.get_movie_by_id(movie.id)

    async def partial_update_movie(
        self,
        movie_id: int,
        update_movie_data: MoviePartialUpdate,
    ) -> Movie | None:
        movie = await self.get_movie_by_id(movie_id)
        if movie is None:
            return None

        for field, value in update_movie_data.model_dump(exclude_unset=True).items():
            setattr(movie, field, value)

        await self.session.commit()
        await self.session.refresh(movie)
        return await self.get_movie_by_id(movie.id)

    async def delete_movie_by_id(self, movie_id: int) -> bool:
        if await self.get_movie_by_id(movie_id) is None:
            return False

        stmt = delete(Movie).where(Movie.id == movie_id)
        await self.session.execute(stmt)
        await self.session.commit()
        return True
