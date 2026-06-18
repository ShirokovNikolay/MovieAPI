import asyncio

from packages.celery.constants import TaskType
from pydantic import EmailStr

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


@app.task(
    name=TaskType.send_confirmation_email_code.value,
)
def send_confirmation_email_code(
    email: EmailStr,
    confirmation_code: str,
) -> None:
    asyncio.run(
        EmailService.send_confirmation_email_code(
            email=email,
            confirmation_code=confirmation_code,
        ),
    )
