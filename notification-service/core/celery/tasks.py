import asyncio
from datetime import time

from core.celery.celery_app import app

from service import EmailService


@app.task(
    name="notification-service.email.send-welcome-email",
)
def send_welcome_email(email: str, name: str) -> None:
    asyncio.run(
        EmailService.send_welcome_email(
            email,
            name,
        )
    )
