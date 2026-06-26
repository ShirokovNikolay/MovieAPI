from celery import Celery
from packages.celery.constants import Queue, TaskType
from packages.config import settings as package_settings

app = Celery(
    "core.celery.celery_app",
    broker=package_settings.rabbitmq.rabbitmq_url,
    backend="redis://redis:6379/0",
    include=["core.celery.tasks"],
)

app.conf.beat_schedule = {
    "run-spam-every-30-seconds": {
        "task": TaskType.create_chain_user_reminder.value,
        "schedule": 30,
        "options": {"queue": Queue.app},
    },
}
