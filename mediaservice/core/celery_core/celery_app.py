from celery import Celery

app = Celery(
    "core.celery_core.celery_app",
    broker="amqp://guest:guest@rabbitmq:5672/%2f",
    include=["core.celery_core.tasks"],
)
