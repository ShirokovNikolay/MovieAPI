from celery import chain
from packages.celery.constants import Queue, TaskType
from packages.celery.utils import sync_run_coroutine_function

from .celery_app import app
from .utils import (
    get_data_to_send_inactive_users_movie_selection,
    invalidate_movie_detail_cache_by_genre_id,
)


@app.task(  # type: ignore[untyped-decorator]
    name=TaskType.get_data_to_send_inactive_users_email.value,
)
def get_data_to_send_inactive_users_email() -> dict:  # type: ignore[type-arg]
    send_inactive_users_email_data = sync_run_coroutine_function(
        get_data_to_send_inactive_users_movie_selection(),
    )
    return send_inactive_users_email_data.model_dump()  # type: ignore[no-any-return]


@app.task(  # type: ignore[untyped-decorator]
    name=TaskType.create_chain_to_notify_inactive_users.value,
)
def create_chain_to_notify_inactive_users() -> None:
    send_inactive_users_email = app.signature(
        TaskType.send_inactive_users_email.value,
        queue=Queue.notification_service.value,
    )
    task_chain = chain(
        get_data_to_send_inactive_users_email.s().set(
            queue=Queue.app.value,
        ),
        send_inactive_users_email,
    )
    task_chain.delay()


@app.task(  # type: ignore[untyped-decorator]
    name=TaskType.invalidate_movie_detail_cache_by_genre.value,
)
def invalidate_movie_detail_cache_by_genre(genre_id: int) -> None:
    sync_run_coroutine_function(
        invalidate_movie_detail_cache_by_genre_id(genre_id),
    )
