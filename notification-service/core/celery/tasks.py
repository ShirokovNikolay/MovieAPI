import asyncio

from packages.celery.constants import TaskType

from core.celery.celery_app import app
from service import EmailService


@app.task(  # type: ignore[untyped-decorator]
    name=TaskType.send_welcome_email.value,
)
def send_welcome_email(email: str, name: str) -> None:
    asyncio.run(
        EmailService.send_welcome_email(
            email,
            name,
        ),
    )
