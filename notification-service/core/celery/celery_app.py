from celery import Celery
from packages.config import settings as package_settings

app = Celery(
    "core.celery.celery_app",
    broker=package_settings.rabbitmq.rabbitmq_url,
    include=["core.celery.tasks"],
)
