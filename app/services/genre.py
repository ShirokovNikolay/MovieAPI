from typing import cast

from sqlalchemy.ext.asyncio import AsyncSession

from core.exceptions.genre import (
    GenreIdAlreadyHasMoviesError,
    GenreIdNotFoundError,
    GenreNameAlreadyExistsError,
)
from repositories import GenreRepository, MovieRepository
from schemas.genre import (
    GenreCreate,
    GenrePartialUpdate,
    GenreResponse,
    GenreResponseList,
    GenreUpdate,
)


class GenreService:
    def __init__(self, session: AsyncSession) -> None:
        self.genre_repository = GenreRepository(session)
        self.movie_repository = MovieRepository(session)

    async def get_genre_by_id(self, genre_id: int) -> GenreResponse:
        genre = await self.genre_repository.get_genre_by_id(genre_id)
        if genre is not None:
            return GenreResponse.model_validate(genre)

        raise GenreIdNotFoundError(genre_id)

    async def get_all_genres(
        self,
        size: int = 10,
        page: int = 1,
    ) -> GenreResponseList:

        genres = [
            GenreResponse.model_validate(genre)
            for genre in await self.genre_repository.get_all_genres(size, page)
        ]
        return GenreResponseList(
            genre_list=genres,
            size=size,
            page=page,
        )

    async def search_genres_by_name(
        self,
        name: str,
        size: int = 10,
        page: int = 1,
    ) -> GenreResponseList:
        genre_list = [
            GenreResponse.model_validate(genre)
            for genre in await self.genre_repository.search_genres_by_name(
                name, size, page,
            )
        ]
        return GenreResponseList(
            genre_list=genre_list,
            size=size,
            page=page,
        )

    async def create_genre(self, create_data: GenreCreate) -> GenreResponse:
        if await self.genre_repository.genre_name_exists(create_data.name):
            raise GenreNameAlreadyExistsError(create_data.name)

        genre = await self.genre_repository.create_genre(create_data)
        return GenreResponse.model_validate(genre)

    async def update_genre(
        self, genre_id: int, update_data: GenreUpdate,
    ) -> GenreResponse:
        genre = await self.genre_repository.get_genre_by_id(genre_id)
        if genre is None:
            raise GenreIdNotFoundError(genre_id)

        if (
            update_data.name != genre.name
            and await self.genre_repository.genre_name_exists(update_data.name)
        ):
            raise GenreNameAlreadyExistsError(update_data.name)

        updated_genre = await self.genre_repository.update_genre(genre_id, update_data)
        return GenreResponse.model_validate(updated_genre)

    async def partial_update_genre(
        self, genre_id: int, update_data: GenrePartialUpdate,
    ) -> GenreResponse:
        genre = await self.genre_repository.get_genre_by_id(genre_id)
        if genre is None:
            raise GenreIdNotFoundError(genre_id)

        if (
            "name" in update_data.model_fields_set
            and update_data.name != genre.name
            and await self.genre_repository.genre_name_exists(
                cast(str, update_data.name),
            )
        ):
            raise GenreNameAlreadyExistsError(cast(str, update_data.name))

        updated_genre = await self.genre_repository.partial_update_genre(
            genre_id, update_data,
        )
        return GenreResponse.model_validate(updated_genre)

    async def delete_genre_by_id(self, genre_id: int) -> None:
        movies = await self.movie_repository.get_movies_by_genre_id(genre_id)
        if movies:
            raise GenreIdAlreadyHasMoviesError(genre_id)

        if not await self.genre_repository.delete_genre_by_id(genre_id):
            raise GenreIdNotFoundError(genre_id)
