from sqlalchemy.ext.asyncio import AsyncSession

from core.exceptions.favorite_movie import (
    FavoriteMovieIdNotFoundError,
    FavoriteMovieNotFoundByUserAndMovieError,
    FavoriteMovieAlreadyExistsByUserAndMovieError,
)
from core.exceptions.movie import MovieIdNotFoundError
from core.exceptions.user import UserIdNotFoundError
from repositories import UserRepository, MovieRepository
from repositories.favorite_movie import FavoriteMovieRepository
from schemas.favorite_movie import (
    FavoriteMovieList,
    FavoriteMovieResponse,
    FavoriteMovieCreate,
)


class FavoriteMovieService:
    def __init__(self, session: AsyncSession):
        self.favorite_movie_repository = FavoriteMovieRepository(session)
        self.user_repository = UserRepository(session)
        self.movie_repository = MovieRepository(session)

    async def get_favorite_movies_by_user_id(
        self,
        user_id: int,
        size: int = 10,
        page: int = 1,
    ) -> FavoriteMovieList:
        if await self.user_repository.user_id_exists(user_id):
            favorite_movies = [
                FavoriteMovieResponse.model_validate(favorite_movie)
                for favorite_movie in await self.favorite_movie_repository.get_favorite_movies_by_user_id(
                    user_id, size, page
                )
            ]
            return FavoriteMovieList(favorite_movie_list=favorite_movies)

        raise UserIdNotFoundError(user_id)

    async def get_favorite_movie_by_id(
        self,
        favorite_movie_id: int,
    ) -> FavoriteMovieResponse:
        favorite_movie = await self.favorite_movie_repository.get_favorite_movie_by_id(
            favorite_movie_id,
        )
        if favorite_movie is not None:
            return FavoriteMovieResponse.model_validate(favorite_movie)
        raise FavoriteMovieIdNotFoundError(favorite_movie_id)

    async def favorite_movie_exists(self, user_id: int, movie_id: int) -> bool:
        return (
            await self.favorite_movie_repository.get_user_favorite_movie(
                user_id, movie_id
            )
            is not None
        )

    async def favorite_movie_exists_by_id(self, favorite_movie_id: int) -> bool:
        return (
            await self.favorite_movie_repository.get_favorite_movie_by_id(
                favorite_movie_id
            )
            is not None
        )

    async def count_favorites_by_movie(self, movie_id: int) -> int:
        if await self.movie_repository.movie_id_exists(movie_id):
            return await self.favorite_movie_repository.count_favorites_by_movie(
                movie_id
            )
        raise MovieIdNotFoundError(movie_id)

    async def create_user_favorite_movie(
        self,
        user_id: int,
        create_favorite_movie_data: FavoriteMovieCreate,
    ) -> FavoriteMovieResponse:
        if not await self.user_repository.user_id_exists(user_id):
            raise UserIdNotFoundError(user_id)

        if not await self.movie_repository.movie_id_exists(
            create_favorite_movie_data.movie_id
        ):
            raise MovieIdNotFoundError(create_favorite_movie_data.movie_id)

        if await self.favorite_movie_repository.favorite_movie_exists(
            user_id, create_favorite_movie_data.movie_id
        ):
            raise FavoriteMovieAlreadyExistsByUserAndMovieError(
                user_id, create_favorite_movie_data.movie_id
            )
        favorite_movie = (
            await self.favorite_movie_repository.create_user_favorite_movie(
                user_id=user_id,
                create_favorite_movie_data=create_favorite_movie_data,
            )
        )
        return FavoriteMovieResponse.model_validate(favorite_movie)

    async def delete_favorite_movie_by_id(self, favorite_movie_id: int) -> None:
        if not await self.favorite_movie_repository.delete_favorite_movie_by_id(
            favorite_movie_id
        ):
            raise FavoriteMovieIdNotFoundError(favorite_movie_id)

    async def delete_user_favorite_movie(self, user_id: int, movie_id: int) -> None:
        if not await self.user_repository.user_id_exists(user_id):
            raise UserIdNotFoundError(user_id)
        if not await self.movie_repository.movie_id_exists(movie_id):
            raise MovieIdNotFoundError(movie_id)
        if not await self.favorite_movie_repository.delete_user_favorite_movie(
            user_id, movie_id
        ):
            raise FavoriteMovieNotFoundByUserAndMovieError(user_id, movie_id)
