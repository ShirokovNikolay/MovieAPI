from celery import Celery
from celery.schedules import crontab
from packages.celery.constants import Queue, TaskType
from packages.config import settings as package_settings

from core.config import settings

app = Celery(
    "core.celery.celery_app",
    broker=package_settings.rabbitmq.url,
    backend="redis://redis:6379/0",
    include=["core.celery.tasks"],
)

app.conf.beat_schedule = {
    "notify-inactive-users-with-movie-picks": {
        "task": TaskType.create_chain_to_notify_inactive_users.value,
        "schedule": crontab(
            day_of_week=settings.celery.beat.notify_inactive_users_with_movie_picks.day_of_week,
            hour=settings.celery.beat.notify_inactive_users_with_movie_picks.hour,
            minute=settings.celery.beat.notify_inactive_users_with_movie_picks.minute,
        ),
        "options": {"queue": Queue.app},
    },
}
