from celery import Celery

app = Celery(
    "core.celery.celery_app",
    broker="amqp://guest:guest@rabbitmq:5672/%2f",
    backend="redis://redis:6379/0",
    include=["core.celery.tasks"],
)

app.conf.beat_schedule = {
    "run-spam-every-30-seconds": {
        "task": "testing",
        "schedule": 5 * 60,
        "options": {"queue": "movie-catalog"},
    },
}
