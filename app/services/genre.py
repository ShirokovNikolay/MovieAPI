from sqlalchemy.ext.asyncio import AsyncSession
from repositories import GenreRepository, MovieRepository
from fastapi import HTTPException, status

from schemas.genre import (
    GenreCreate,
    GenreUpdate,
    GenreResponse,
    GenrePartialUpdate,
    GenreResponseList,
)


class GenreService:
    def __init__(self, session: AsyncSession) -> None:
        self.genre_repository = GenreRepository(session)
        self.movie_repository = MovieRepository(session)

    async def get_genre_by_id(self, genre_id: int) -> GenreResponse:
        genre = await self.genre_repository.get_genre_by_id(genre_id)
        if genre is not None:
            return GenreResponse.model_validate(genre)

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Genre with {genre_id=} does not exist",
        )

    async def get_genre_by_name(self, genre_name: str) -> GenreResponse:
        genre = await self.genre_repository.get_genre_by_name(genre_name)
        if genre is not None:
            return GenreResponse.model_validate(genre)

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Genre with {genre_name=} does not exist",
        )

    async def get_all_genres(self) -> GenreResponseList:
        genres = [
            GenreResponse.model_validate(genre)
            for genre in await self.genre_repository.get_all_genres()
        ]
        return GenreResponseList(genre_list=genres)

    async def create_genre(self, create_data: GenreCreate) -> GenreResponse:
        if await self.genre_repository.genre_name_exists(create_data.name):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Genre with genre_name={create_data.name} already exists",
            )

        genre = await self.genre_repository.create_genre(create_data)
        return GenreResponse.model_validate(genre)

    async def update_genre(
        self, genre_id: int, update_data: GenreUpdate
    ) -> GenreResponse:
        genre = await self.genre_repository.get_genre_by_id(genre_id)
        if genre is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Genre with {genre_id=} not found",
            )

        if (
            update_data.name != genre.name
            and await self.genre_repository.genre_name_exists(update_data.name)
        ):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Genre with genre_name={update_data.name} already exists",
            )
        updated_genre = await self.genre_repository.update_genre(genre_id, update_data)
        return GenreResponse.model_validate(updated_genre)

    async def partial_update_genre(
        self, genre_id: int, update_data: GenrePartialUpdate
    ) -> GenreResponse:
        genre = await self.genre_repository.get_genre_by_id(genre_id)
        if genre is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Genre with {genre_id=} not found",
            )

        if (
            "name" in update_data.model_fields_set
            and update_data.name != genre.name
            and self.genre_repository.genre_name_exists(update_data.name)
        ):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Genre with genre_name={update_data.name} already exists",
            )
        updated_genre = await self.genre_repository.partial_update_genre(
            genre_id, update_data
        )
        return GenreResponse.model_validate(updated_genre)

    async def delete_genre_by_id(self, genre_id: int) -> None:
        movies = await self.movie_repository.get_movies_by_genre_id(genre_id)
        if movies:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Movies with {genre_id=} already exist",
            )

        if not await self.genre_repository.delete_genre_by_id(genre_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Genre with {genre_id=} does not exist",
            )

    async def delete_genre_by_name(self, genre_name: str) -> None:
        movies = await self.movie_repository.get_movies_by_genre_name(genre_name)
        if movies:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Movies with {genre_name=} already exist",
            )

        if not await self.genre_repository.delete_genre_by_name(genre_name):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Genre with {genre_name=} does not exist",
            )
