import asyncio
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from celery import chord, group
from packages.celery.constants import Queue, TaskType
from packages.schemas import MovieEmailSendDataList, UserEmailSendDataList

from core.constants import SortMonotony, SortType
from core.rabbitmq.utils import get_session, get_user_service
from schemas.movie import MovieFilter
from services import MovieService

from .celery_app import app


@asynccontextmanager
async def get_movie_service() -> AsyncGenerator[MovieService]:
    async with get_session() as session:
        movie_service = MovieService(session)
        yield movie_service


async def get_inactive_users() -> UserEmailSendDataList:
    async with get_user_service() as user_service:
        return await user_service.get_inactive_users()


async def get_newest_movies() -> MovieEmailSendDataList:
    async with get_movie_service() as movie_service:
        movie_filter = MovieFilter(
            sort_by=SortType.date.value,
            sorting_direction=SortMonotony.descending.value,
        )

        return await movie_service.search_movies_with_filters(
            movie_filter=movie_filter,
        )


@app.task(
    name=TaskType.prepare_inactive_users.value,
)
def prepare_inactive_users() -> dict:
    loop = asyncio.new_event_loop()
    result = loop.run_until_complete(get_inactive_users())
    loop.close()
    return result.model_dump()


@app.task(
    name=TaskType.prepare_newest_movies.value,
)
def prepare_newest_movies() -> dict:
    loop = asyncio.new_event_loop()
    result = loop.run_until_complete(get_newest_movies())
    loop.close()
    return result.model_dump()


@app.task(
    name=TaskType.create_chain_user_reminder.value,
)
def test() -> None:
    chained_group = group(
        prepare_inactive_users.s().set(queue=Queue.app.value),
        prepare_newest_movies.s().set(queue=Queue.app.value),
    )

    notify = app.signature(
        TaskType.send_inactive_user_reminder.value,
        queue=Queue.notification.value,
    )
    chord(chained_group)(notify)
