from typing import cast

from sqlalchemy import and_, delete, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from models import FavoriteMovie, User
from schemas.favorite_movie import FavoriteMovieCreate


class FavoriteMovieRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_favorite_movie_by_id(
        self,
        favorite_movie_id: int,
    ) -> FavoriteMovie | None:
        stmt = (
            select(FavoriteMovie)
            .options(
                joinedload(FavoriteMovie.movie),
            )
            .where(FavoriteMovie.id == favorite_movie_id)
        )
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def get_favorite_movie_owner(self, favorite_movie_id: int) -> User | None:
        stmt = (
            select(User)
            .join(FavoriteMovie, User.id == FavoriteMovie.user_id)
            .where(FavoriteMovie.id == favorite_movie_id)
        )
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def get_favorite_movies_by_user_id(
        self,
        user_id: int,
        size: int = 10,
        page: int = 1,
    ) -> list[FavoriteMovie]:
        stmt = (
            select(FavoriteMovie)
            .options(
                joinedload(FavoriteMovie.movie),
            )
            .where(
                FavoriteMovie.user_id == user_id,
            )
            .limit(size)
            .offset(size * (page - 1))
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def get_user_favorite_movie(
        self,
        user_id: int,
        movie_id: int,
    ) -> FavoriteMovie | None:
        stmt = (
            select(FavoriteMovie)
            .options(joinedload(FavoriteMovie.movie))
            .where(
                and_(
                    FavoriteMovie.user_id == user_id,
                    FavoriteMovie.movie_id == movie_id,
                ),
            )
        )
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def favorite_movie_exists(self, user_id: int, movie_id: int) -> bool:
        return await self.get_user_favorite_movie(user_id, movie_id) is not None

    async def count_favorites_by_movie(self, movie_id: int) -> int:
        stmt = select(func.count(FavoriteMovie.id)).where(
            FavoriteMovie.movie_id == movie_id,
        )
        result = await self.session.execute(stmt)
        return cast(int, result.scalar())

    async def create_user_favorite_movie(
        self,
        user_id: int,
        create_favorite_movie_data: FavoriteMovieCreate,
    ) -> FavoriteMovie | None:
        favorite_movie = FavoriteMovie(
            user_id=user_id,
            **create_favorite_movie_data.model_dump(),
        )
        self.session.add(favorite_movie)
        await self.session.commit()
        await self.session.refresh(favorite_movie)
        return await self.get_favorite_movie_by_id(favorite_movie.id)

    async def delete_favorite_movie_by_id(
        self, favorite_movie_id: int,
    ) -> FavoriteMovie | None:
        favorite_movie = await self.get_favorite_movie_by_id(favorite_movie_id)
        if favorite_movie is None:
            return None
        stmt = delete(FavoriteMovie).where(FavoriteMovie.id == favorite_movie_id)
        await self.session.execute(stmt)
        await self.session.commit()
        return favorite_movie

    async def delete_user_favorite_movie(
        self, user_id: int, movie_id: int,
    ) -> FavoriteMovie | None:
        favorite_movie = await self.get_user_favorite_movie(
            user_id=user_id, movie_id=movie_id,
        )
        if favorite_movie is None:
            return None

        stmt = delete(FavoriteMovie).where(
            and_(
                FavoriteMovie.user_id == user_id,
                FavoriteMovie.movie_id == movie_id,
            ),
        )
        await self.session.execute(stmt)
        await self.session.commit()
        return favorite_movie
