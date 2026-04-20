from datetime import datetime
from typing import cast

from sqlalchemy.ext.asyncio import AsyncSession

from core.exceptions.genre import GenreIdNotFoundError
from core.exceptions.user import UserIdNotFoundError
from repositories import MovieRepository, GenreRepository, UserRepository
from repositories.watch_history import WatchHistoryRepository
from schemas.movie import (
    MovieResponse,
    MovieResponseList,
    MovieCreate,
    MovieUpdate,
    MoviePartialUpdate,
)

from core.exceptions.movie import (
    MovieIdNotFoundError,
    MovieNameAlreadyExistsError,
)
from schemas.watch_history import WatchHistoryCreate


class MovieService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.user_repository = UserRepository(session)
        self.movie_repository = MovieRepository(session)
        self.genre_repository = GenreRepository(session)
        self.watch_history_repository = WatchHistoryRepository(session)

    async def get_movie_by_id(self, movie_id: int) -> MovieResponse:
        movie = await self.movie_repository.get_movie_by_id(movie_id)
        if movie is not None:
            return MovieResponse.model_validate(movie)

        raise MovieIdNotFoundError(movie_id)

    async def watch_movie(
        self,
        user_id: int,
        create_watch_history_data: WatchHistoryCreate,
    ) -> MovieResponse:
        if not await self.user_repository.user_id_exists(user_id):
            raise UserIdNotFoundError(user_id)

        movie = await self.movie_repository.get_movie_by_id(
            movie_id=create_watch_history_data.movie_id
        )
        if movie is None:
            raise MovieIdNotFoundError(create_watch_history_data.movie_id)

        await self.watch_history_repository.add_movie_to_watch_history(
            user_id,
            create_watch_history_data,
        )
        await self.session.refresh(movie)
        return MovieResponse.model_validate(movie)

    async def get_movies(
        self,
        size: int = 10,
        page: int = 1,
    ) -> MovieResponseList:
        movies = [
            MovieResponse.model_validate(movie)
            for movie in await self.movie_repository.get_movies(size, page)
        ]
        return MovieResponseList(
            movie_list=movies,
            size=size,
            page=page,
        )

    async def get_movies_by_genre_id(
        self,
        genre_id: int,
        size: int = 10,
        page: int = 1,
    ) -> MovieResponseList:
        if not await self.genre_repository.genre_id_exists(genre_id):
            raise MovieIdNotFoundError(genre_id)

        movies = [
            MovieResponse.model_validate(movie)
            for movie in await self.movie_repository.get_movies_by_genre_id(
                genre_id,
                size,
                page,
            )
        ]
        return MovieResponseList(
            movie_list=movies,
            size=size,
            page=page,
        )

    async def search_movies_by_name(
        self,
        name: str,
        size: int = 10,
        page: int = 1,
    ) -> MovieResponseList:
        movie_list = [
            MovieResponse.model_validate(movie)
            for movie in await self.movie_repository.search_movies_by_name(
                name,
                size,
                page,
            )
        ]
        return MovieResponseList(
            movie_list=movie_list,
            size=size,
            page=page,
        )

    async def get_movies_by_rating_range(
        self,
        min_rating: int,
        max_rating: int,
        size: int = 10,
        page: int = 1,
    ) -> MovieResponseList:
        movies = [
            MovieResponse.model_validate(movie)
            for movie in await self.movie_repository.get_movies_by_rating_range(
                min_rating,
                max_rating,
                size,
                page,
            )
        ]
        return MovieResponseList(
            movie_list=movies,
            size=size,
            page=page,
        )

    async def get_movies_by_year(
        self,
        year: int,
        size: int = 10,
        page: int = 1,
    ) -> MovieResponseList:
        movies = [
            MovieResponse.model_validate(movie)
            for movie in await self.movie_repository.get_movies_by_year(
                year,
                size,
                page,
            )
        ]
        return MovieResponseList(
            movie_list=movies,
            size=size,
            page=page,
        )

    async def get_movies_by_release_date_range(
        self,
        release_date_start: datetime,
        release_date_end: datetime,
        size: int = 10,
        page: int = 1,
    ) -> MovieResponseList:
        movies = [
            MovieResponse.model_validate(movie)
            for movie in await self.movie_repository.get_movies_by_release_date(
                release_date_start,
                release_date_end,
                size=size,
                page=page,
            )
        ]
        return MovieResponseList(
            movie_list=movies,
            size=size,
            page=page,
        )

    async def get_top_rated_movies(self, limit: int) -> MovieResponseList:
        movies = [
            MovieResponse.model_validate(movie)
            for movie in await self.movie_repository.get_top_rated_movies(limit)
        ]
        return MovieResponseList(
            movie_list=movies,
            size=limit,
        )

    async def get_top_newest_movies(self, limit: int) -> MovieResponseList:
        movies = [
            MovieResponse.model_validate(movie)
            for movie in await self.movie_repository.get_top_newest_movies(limit)
        ]
        return MovieResponseList(
            movie_list=movies,
            size=limit,
        )

    async def get_top_oldest_movies(self, limit: int) -> MovieResponseList:
        movies = [
            MovieResponse.model_validate(movie)
            for movie in await self.movie_repository.get_top_oldest_movies(limit)
        ]
        return MovieResponseList(
            movie_list=movies,
            size=limit,
        )

    async def create_movie(self, create_movie_data: MovieCreate) -> MovieResponse:
        if await self.movie_repository.movie_name_exists(create_movie_data.name):
            raise MovieNameAlreadyExistsError(create_movie_data.name)

        if not await self.genre_repository.genre_id_exists(create_movie_data.genre_id):
            raise GenreIdNotFoundError(create_movie_data.genre_id)

        movie = await self.movie_repository.create_movie(create_movie_data)
        return MovieResponse.model_validate(movie)

    async def update_movie(
        self,
        movie_id: int,
        update_movie_data: MovieUpdate,
    ) -> MovieResponse:
        movie = await self.movie_repository.get_movie_by_id(movie_id)
        if movie is None:
            raise MovieIdNotFoundError(movie_id)

        if not await self.genre_repository.genre_id_exists(update_movie_data.genre_id):
            raise GenreIdNotFoundError(update_movie_data.genre_id)

        if (
            movie.name != update_movie_data.name
            and await self.movie_repository.movie_name_exists(update_movie_data.name)
        ):
            raise MovieNameAlreadyExistsError(update_movie_data.name)

        updated_movie = await self.movie_repository.update_movie(
            movie_id, update_movie_data
        )
        return MovieResponse.model_validate(updated_movie)

    async def partial_update_movie(
        self,
        movie_id: int,
        update_movie_data: MoviePartialUpdate,
    ) -> MovieResponse:
        movie = await self.movie_repository.get_movie_by_id(movie_id)
        if movie is None:
            raise MovieIdNotFoundError(movie_id)

        if (
            "genre_id" in update_movie_data.model_fields_set
            and not await self.genre_repository.genre_id_exists(
                cast(int, update_movie_data.genre_id)
            )
        ):
            raise GenreIdNotFoundError(
                cast(int, update_movie_data.genre_id),
            )

        if (
            "name" in update_movie_data.model_fields_set
            and movie.name != update_movie_data.name
            and await self.movie_repository.movie_name_exists(
                cast(str, update_movie_data.name)
            )
        ):
            raise MovieNameAlreadyExistsError(cast(str, update_movie_data.name))

        updated_movie = await self.movie_repository.partial_update_movie(
            movie_id, update_movie_data
        )
        return MovieResponse.model_validate(updated_movie)

    async def delete_movie_by_id(self, movie_id: int) -> None:
        if not await self.movie_repository.delete_movie_by_id(movie_id):
            raise MovieIdNotFoundError(movie_id)
