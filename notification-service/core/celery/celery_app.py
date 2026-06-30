from celery import Celery
from packages.config import settings as package_settings

from core.constants import CELERY_APP_MODULE, CELERY_TASKS_MODULES

app = Celery(
    CELERY_APP_MODULE,
    broker=package_settings.rabbitmq.url,
    backend=package_settings.redis.url,
    include=CELERY_TASKS_MODULES,
)
