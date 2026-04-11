from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete

from models import Genre
from schemas.genre import GenreCreate, GenreUpdate, GenrePartialUpdate


class GenreRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_genre_by_id(self, genre_id: int) -> Genre | None:
        stmt = select(Genre).where(Genre.id == genre_id)
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def get_all_genres(
        self,
        size: int = 10,
        page: int = 1,
    ) -> list[Genre]:
        stmt = select(Genre).limit(size).offset(size * (page - 1))
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def search_genres_by_name(
        self,
        name: str,
        size: int = 10,
        page: int = 1,
    ) -> list[Genre]:
        stmt = (
            select(Genre)
            .where(Genre.name.ilike("%" + name + "%"))
            .limit(size)
            .offset(size * (page - 1))
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def get_genre_by_name(self, name: str) -> Genre | None:
        stmt = select(Genre).where(Genre.name == name)
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def genre_id_exists(self, genre_id: int) -> bool:
        return await self.get_genre_by_id(genre_id) is not None

    async def genre_name_exists(self, name: str) -> bool:
        return await self.get_genre_by_name(name) is not None

    async def create_genre(self, create_data: GenreCreate) -> Genre:
        genre = Genre(**create_data.model_dump())
        self.session.add(genre)
        await self.session.commit()
        await self.session.refresh(genre)
        return genre

    async def update_genre(
        self,
        genre_id: int,
        update_data: GenreUpdate,
    ) -> Genre | None:
        genre = await self.get_genre_by_id(genre_id)
        if not genre:
            return None
        for field, value in update_data.model_dump().items():
            setattr(genre, field, value)

        await self.session.commit()
        await self.session.refresh(genre)
        return genre

    async def partial_update_genre(
        self,
        genre_id: int,
        update_data: GenrePartialUpdate,
    ) -> Genre | None:
        genre = await self.get_genre_by_id(genre_id)
        if not genre:
            return None

        for field, value in update_data.model_dump(exclude_unset=True).items():
            setattr(genre, field, value)

        await self.session.commit()
        await self.session.refresh(genre)
        return genre

    async def delete_genre_by_id(self, genre_id: int) -> bool:
        if await self.get_genre_by_id(genre_id) is None:
            return False
        stmt = delete(Genre).where(Genre.id == genre_id)
        await self.session.execute(stmt)
        await self.session.commit()
        return True
