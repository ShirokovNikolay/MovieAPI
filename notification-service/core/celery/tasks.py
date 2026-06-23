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


@app.task(  # type: ignore[untyped-decorator]
    name=TaskType.send_confirm_registration_email.value,
)
def send_confirm_registration_email(
    email: EmailStr,
    confirmation_code: str,
) -> None:
    asyncio.run(
        EmailService.send_confirm_registration_email(
            email,
            confirmation_code,
        ),
    )


@app.task(  # type: ignore[untyped-decorator]
    name=TaskType.send_confirm_login_email.value,
)
def send_confirm_login_email(
    email: EmailStr,
    confirmation_code: str,
) -> None:
    asyncio.run(
        EmailService.send_confirm_login_email(
            email=email,
            confirmation_code=confirmation_code,
        ),
    )


@app.task(  # type: ignore[untyped-decorator]
    name=TaskType.send_reset_password_email_data.value,
)
def send_reset_password_email_data(
    login: str,
    email: EmailStr,
    confirmation_code: str,
) -> None:
    asyncio.run(
        EmailService.send_reset_password_email_data(
            login=login,
            email=email,
            confirmation_code=confirmation_code,
        ),
    )
