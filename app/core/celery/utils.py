import asyncio
from asyncio import gather

from packages.rabbitmq.connection import rabbitmq_connection_startup
from packages.schemas.notification import (
    InactiveUser,
    InactiveUserList,
    SelectedMovie,
    SelectedMovieList,
    SendInactiveUsersMovieSelectionData,
)

from core.constants import INACTIVE_DAYS, CacheEntity, SortMonotony, SortType
from core.utils import (
    get_cache_key_service,
    get_movie_redis_service,
    get_movie_service,
    get_user_service,
)
from schemas.movie import MovieFilter


async def get_inactive_users(days: int) -> InactiveUserList:
    async with get_user_service() as user_service:
        inactive_users = await user_service.get_inactive_users(days=days)
        inactive_user_list = [
            InactiveUser(
                name=user.name,
                email=user.email,
            )
            for user in inactive_users.user_list
        ]
        return InactiveUserList(inactive_user_list=inactive_user_list)


async def get_movie_selection() -> SelectedMovieList:
    await rabbitmq_connection_startup()
    async with get_movie_service() as movie_service:
        movie_filter = MovieFilter(
            sort_by=SortType.date.value,
            sorting_direction=SortMonotony.descending.value,
        )
        selected_movies = await movie_service.search_movies_with_filters(
            movie_filter=movie_filter,
        )
        movie_selection = [
            SelectedMovie(
                name=movie.name,
                genre_name=movie.genre.name,
                rating=movie.rating,
                source_url=movie.source_url,
                release_date=movie.release_date,
            )
            for movie in selected_movies.movie_list
        ]
        return SelectedMovieList(
            selected_movie_list=movie_selection,
        )


async def get_data_to_send_inactive_users_movie_selection() -> (
    SendInactiveUsersMovieSelectionData
):
    inactive_users, movie_selection = await gather(
        get_inactive_users(days=INACTIVE_DAYS),
        get_movie_selection(),
    )
    return SendInactiveUsersMovieSelectionData(
        inactive_users=inactive_users,
        movie_selection=movie_selection,
    )


async def invalidate_movie_detail_cache_by_genre_id(genre_id: int) -> None:
    await rabbitmq_connection_startup()
    async with (
        get_movie_service() as movie_service,
        get_movie_redis_service() as movie_redis_service,
        get_cache_key_service() as cache_key_service,
    ):
        movies = await movie_service.get_movies_by_genre_id(genre_id=genre_id)
        invalidate_movie_keys = []
        for movie in movies.movie_list:
            movie_key = cache_key_service.build_item_key(
                entity=CacheEntity.movie,
                entity_id=movie.id,
                action="get",
            )
            invalidate_movie_keys.append(movie_key)

        await movie_redis_service.delete_list_of_keys(invalidate_movie_keys)


async def invalidate_reviews_cache_on_update_user(user_id: int) -> None:
    await rabbitmq_connection_startup()
    async with (
        get_movie_service() as movie_service,
        get_cache_key_service() as cache_key_service,
    ):
        movies = await movie_service.get_movies_reviewed_by_user(user_id=user_id)
        invalidate_review_coroutines = []
        for movie in movies.movie_list:
            coroutine = cache_key_service.invalidate_list_keys(
                entity=CacheEntity.review,
                movie_id=movie.id,
            )
            invalidate_review_coroutines.append(coroutine)

        await asyncio.gather(*invalidate_review_coroutines)
