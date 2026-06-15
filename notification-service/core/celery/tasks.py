import asyncio

from core.celery.celery_app import app
from service import EmailService


@app.task(  # type: ignore[untyped-decorator]
    name="notification-service.email.send-welcome-email",
)
def send_welcome_email(email: str, name: str) -> None:
    asyncio.run(
        EmailService.send_welcome_email(
            email,
            name,
        ),
    )
