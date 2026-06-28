from celery import chain
from packages.celery.constants import Queue, TaskType
from packages.celery.utils import sync_run_coroutine_function

from .celery_app import app
from .utils import get_data_to_send_inactive_users_movie_selection


@app.task(
    name=TaskType.get_data_to_send_inactive_users_email.value,
)
def get_data_to_send_inactive_users_email() -> dict:
    send_inactive_users_email_data = sync_run_coroutine_function(
        get_data_to_send_inactive_users_movie_selection(),
    )
    return send_inactive_users_email_data.model_dump()


@app.task(
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
    task_chain.apply_async()
