from asyncio import gather

from packages.rabbitmq.connection import rabbitmq_connection_startup
from packages.schemas.notification import (
    InactiveUser,
    InactiveUserList,
    SelectedMovie,
    SelectedMovieList,
    SendInactiveUsersMovieSelectionData,
)

from core.constants import INACTIVE_DAYS, SortMonotony, SortType
from core.utils import get_movie_service, get_user_service
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
