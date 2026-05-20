from datetime import datetime
from typing import cast

from sqlalchemy.ext.asyncio import AsyncSession

from core.exceptions.genre import GenreIdNotFoundError
from core.exceptions.movie import (
    MovieIdNotFoundError,
    MovieNameAlreadyExistsError,
)
from core.exceptions.user import UserIdNotFoundError
from dependencies.annotations.validators import PaginationPageDep, PaginationSizeDep
from repositories import GenreRepository, MovieRepository, UserRepository
from repositories.watch_history import WatchHistoryRepository
from schemas.movie import (
    MovieCreate,
    MovieFilter,
    MoviePartialUpdate,
    MovieResponse,
    MovieResponseList,
    MovieUpdate,
    MovieWithGenreResponse,
    MovieWithGenreResponseList,
)
from schemas.watch_history import WatchHistoryCreate


class MovieService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.user_repository = UserRepository(session)
        self.movie_repository = MovieRepository(session)
        self.genre_repository = GenreRepository(session)
        self.watch_history_repository = WatchHistoryRepository(session)

    async def get_movie_by_id(self, movie_id: int) -> MovieWithGenreResponse:
        movie = await self.movie_repository.get_movie_by_id(movie_id)
        if movie is not None:
            return MovieWithGenreResponse.model_validate(movie)

        raise MovieIdNotFoundError(movie_id)

    async def watch_movie(
        self,
        user_id: int,
        create_watch_history_data: WatchHistoryCreate,
    ) -> MovieWithGenreResponse:
        if not await self.user_repository.user_id_exists(user_id):
            raise UserIdNotFoundError(user_id)

        movie = await self.movie_repository.get_movie_by_id(
            movie_id=create_watch_history_data.movie_id,
        )
        if movie is None:
            raise MovieIdNotFoundError(create_watch_history_data.movie_id)

        await self.watch_history_repository.add_movie_to_watch_history(
            user_id,
            create_watch_history_data,
        )
        await self.session.refresh(movie)
        return MovieWithGenreResponse.model_validate(movie)

    async def get_movies(
        self,
        size: int = 10,
        page: int = 1,
    ) -> MovieWithGenreResponseList:
        movies = [
            MovieWithGenreResponse.model_validate(movie)
            for movie in await self.movie_repository.get_movies(size, page)
        ]
        return MovieWithGenreResponseList(
            movie_list=movies,
            size=size,
            page=page,
        )

    async def search_movies_with_filters(
        self,
        movie_filter: MovieFilter,
        size: PaginationSizeDep = 10,
        page: PaginationPageDep = 1,
    ) -> MovieWithGenreResponseList:
        movies = [
            MovieWithGenreResponse.model_validate(movie)
            for movie in await self.movie_repository.search_movies_with_filters(
                movie_filter,
                size,
                page,
            )
        ]
        return MovieWithGenreResponseList(
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
    ) -> MovieWithGenreResponseList:
        movie_list = [
            MovieWithGenreResponse.model_validate(movie)
            for movie in await self.movie_repository.search_movies_by_name(
                name,
                size,
                page,
            )
        ]
        return MovieWithGenreResponseList(
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
    ) -> MovieWithGenreResponseList:
        movies = [
            MovieWithGenreResponse.model_validate(movie)
            for movie in await self.movie_repository.get_movies_by_rating_range(
                min_rating,
                max_rating,
                size,
                page,
            )
        ]
        return MovieWithGenreResponseList(
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
    ) -> MovieWithGenreResponseList:
        movies = [
            MovieWithGenreResponse.model_validate(movie)
            for movie in await self.movie_repository.get_movies_by_release_date(
                release_date_start,
                release_date_end,
                size=size,
                page=page,
            )
        ]
        return MovieWithGenreResponseList(
            movie_list=movies,
            size=size,
            page=page,
        )

    async def get_top_rated_movies(
        self,
        size: int,
        page: int,
    ) -> MovieWithGenreResponseList:
        movies = [
            MovieWithGenreResponse.model_validate(movie)
            for movie in await self.movie_repository.get_top_rated_movies(size, page)
        ]
        return MovieWithGenreResponseList(
            movie_list=movies,
            size=size,
            page=page,
        )

    async def get_top_newest_movies(
        self,
        size: int,
        page: int,
    ) -> MovieWithGenreResponseList:
        movies = [
            MovieWithGenreResponse.model_validate(movie)
            for movie in await self.movie_repository.get_top_newest_movies(size, page)
        ]
        return MovieWithGenreResponseList(
            movie_list=movies,
            size=size,
            page=page,
        )

    async def get_top_oldest_movies(
        self,
        size: int,
        page: int,
    ) -> MovieWithGenreResponseList:
        movies = [
            MovieWithGenreResponse.model_validate(movie)
            for movie in await self.movie_repository.get_top_oldest_movies(size, page)
        ]
        return MovieWithGenreResponseList(
            movie_list=movies,
            size=size,
            page=page,
        )

    async def create_movie(
        self,
        create_movie_data: MovieCreate,
    ) -> MovieWithGenreResponse:
        if await self.movie_repository.movie_name_exists(create_movie_data.name):
            raise MovieNameAlreadyExistsError(create_movie_data.name)

        if not await self.genre_repository.genre_id_exists(create_movie_data.genre_id):
            raise GenreIdNotFoundError(create_movie_data.genre_id)

        movie = await self.movie_repository.create_movie(create_movie_data)
        return MovieWithGenreResponse.model_validate(movie)

    async def update_movie(
        self,
        movie_id: int,
        update_movie_data: MovieUpdate,
    ) -> MovieWithGenreResponse:
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
            movie_id,
            update_movie_data,
        )
        return MovieWithGenreResponse.model_validate(updated_movie)

    async def partial_update_movie(
        self,
        movie_id: int,
        update_movie_data: MoviePartialUpdate,
    ) -> MovieWithGenreResponse:
        movie = await self.movie_repository.get_movie_by_id(movie_id)
        if movie is None:
            raise MovieIdNotFoundError(movie_id)

        if (
            "genre_id" in update_movie_data.model_fields_set
            and not await self.genre_repository.genre_id_exists(
                cast(int, update_movie_data.genre_id),
            )
        ):
            raise GenreIdNotFoundError(
                cast(int, update_movie_data.genre_id),
            )

        if (
            "name" in update_movie_data.model_fields_set
            and movie.name != update_movie_data.name
            and await self.movie_repository.movie_name_exists(
                cast(str, update_movie_data.name),
            )
        ):
            raise MovieNameAlreadyExistsError(cast(str, update_movie_data.name))

        updated_movie = await self.movie_repository.partial_update_movie(
            movie_id,
            update_movie_data,
        )
        return MovieWithGenreResponse.model_validate(updated_movie)

    async def delete_movie_by_id(self, movie_id: int) -> None:
        if not await self.movie_repository.delete_movie_by_id(movie_id):
            raise MovieIdNotFoundError(movie_id)
