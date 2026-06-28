from celery import Celery
from packages.config import settings as package_settings

app = Celery(
    "core.celery.celery_app",
    broker=package_settings.rabbitmq.url,
    backend="redis://redis:6379/0",
    include=["core.celery.tasks"],
)
