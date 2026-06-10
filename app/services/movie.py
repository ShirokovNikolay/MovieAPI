from typing import cast

from packages.constants import Exchange, ExchangeType, Queue
from packages.rabbitmq import RabbitMQService
from packages.rabbitmq.utils import create_message
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
    def __init__(
        self,
        session: AsyncSession,
        rabbitmq_service: RabbitMQService,
    ) -> None:
        self.session = session
        self.user_repository = UserRepository(session)
        self.movie_repository = MovieRepository(session)
        self.genre_repository = GenreRepository(session)
        self.watch_history_repository = WatchHistoryRepository(session)
        self.rabbitmq_service = rabbitmq_service

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

    async def create_movie(
        self,
        create_movie_data: MovieCreate,
    ) -> MovieWithGenreResponse:
        if await self.movie_repository.movie_name_exists(create_movie_data.name):
            raise MovieNameAlreadyExistsError(create_movie_data.name)

        if not await self.genre_repository.genre_id_exists(create_movie_data.genre_id):
            raise GenreIdNotFoundError(create_movie_data.genre_id)

        movie = await self.movie_repository.create_movie(create_movie_data)
        exchange = await self.rabbitmq_service.declare_exchange(
            name=Exchange.app.value,
            type=ExchangeType.direct.value,
            durable=True,
        )
        body = {
            "entity_id": movie.id,
            "object_url": create_movie_data.preview_url,
        }
        message = create_message(body=body)
        await self.rabbitmq_service.publish(
            message=message,
            exchange=exchange,
            routing_key=Queue.copy_file.value,
        )

        body = {
            "entity_id": movie.id,
            "object_url": create_movie_data.source_url,
        }
        message = create_message(body=body)
        await self.rabbitmq_service.publish(
            message=message,
            exchange=exchange,
            routing_key=Queue.copy_file.value,
        )
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

        current_movie_preview_url = movie.preview_url
        current_movie_source_url = movie.source_url
        updated_movie = await self.movie_repository.update_movie(
            movie_id,
            update_movie_data,
        )

        exchange = await self.rabbitmq_service.declare_exchange(
            name=Exchange.app.value,
            type=ExchangeType.direct.value,
            durable=True,
        )

        if current_movie_preview_url != update_movie_data.preview_url:
            body = {
                "entity_id": movie.id,
                "object_url": update_movie_data.preview_url,
            }
            message = create_message(body=body)
            await self.rabbitmq_service.publish(
                message=message,
                exchange=exchange,
                routing_key=Queue.copy_file.value,
            )

            body = {
                "object_url": current_movie_preview_url,
            }
            message = create_message(body=body)
            await self.rabbitmq_service.publish(
                message=message,
                exchange=exchange,
                routing_key=Queue.delete_file.value,
            )

        if current_movie_source_url != update_movie_data.source_url:
            body = {
                "entity_id": movie.id,
                "object_url": update_movie_data.source_url,
            }
            message = create_message(body=body)
            await self.rabbitmq_service.publish(
                message=message,
                exchange=exchange,
                routing_key=Queue.copy_file.value,
            )

            body = {
                "object_url": current_movie_source_url,
            }
            message = create_message(body=body)
            await self.rabbitmq_service.publish(
                message=message,
                exchange=exchange,
                routing_key=Queue.delete_file.value,
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
        movie = await self.get_movie_by_id(movie_id)
        if not await self.movie_repository.delete_movie_by_id(movie_id):
            raise MovieIdNotFoundError(movie_id)

        exchange = await self.rabbitmq_service.declare_exchange(
            name=Exchange.app.value,
            type=ExchangeType.direct.value,
            durable=True,
        )
        body = {"object_url": movie.preview_url}
        message = create_message(body=body)
        await self.rabbitmq_service.publish(
            message=message,
            exchange=exchange,
            routing_key=Queue.delete_file.value,
        )

        body = {"object_url": movie.source_url}
        message = create_message(body=body)
        await self.rabbitmq_service.publish(
            message=message,
            exchange=exchange,
            routing_key=Queue.delete_file.value,
        )
