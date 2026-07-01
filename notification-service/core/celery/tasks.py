from packages.celery.constants import TaskType
from packages.celery.utils import sync_run_coroutine_function
from packages.schemas.notification import (
    SendInactiveUsersMovieSelectionData,
)
from pydantic import EmailStr

from core.celery.celery_app import app
from service import EmailService


@app.task(  # type: ignore[untyped-decorator]
    name=TaskType.send_welcome_email.value,
)
def send_welcome_email(email: str, name: str) -> None:
    sync_run_coroutine_function(
        EmailService.send_welcome_email(
            email,
            name,
        ),
    )


@app.task(  # type: ignore[untyped-decorator]
    name=TaskType.send_registration_confirmation_code_email.value,
)
def send_registration_confirmation_code_email(
    email: EmailStr,
    confirmation_code: str,
) -> None:
    sync_run_coroutine_function(
        EmailService.send_registration_confirmation_code_email(
            email,
            confirmation_code,
        ),
    )


@app.task(  # type: ignore[untyped-decorator]
    name=TaskType.send_auth_confirmation_code_email.value,
)
def send_auth_confirmation_code_email(
    email: EmailStr,
    confirmation_code: str,
) -> None:
    sync_run_coroutine_function(
        EmailService.send_auth_confirmation_code_email(
            email=email,
            confirmation_code=confirmation_code,
        ),
    )


@app.task(  # type: ignore[untyped-decorator]
    name=TaskType.send_reset_password_confirmation_code_email.value,
)
def send_reset_password_confirmation_code_email(
    login: str,
    email: EmailStr,
    confirmation_code: str,
) -> None:
    sync_run_coroutine_function(
        EmailService.send_reset_password_confirmation_code_email(
            login=login,
            email=email,
            confirmation_code=confirmation_code,
        ),
    )


@app.task(  # type: ignore[untyped-decorator]
    name=TaskType.send_inactive_users_email.value,
)
def send_inactive_users_email(send_inactive_users_email_data: dict) -> None:  # type: ignore[type-arg]
    send_inactive_users_movie_selection_data = (
        SendInactiveUsersMovieSelectionData.model_validate(
            send_inactive_users_email_data,
        )
    )

    inactive_users = send_inactive_users_movie_selection_data.inactive_users
    movie_selection = send_inactive_users_movie_selection_data.movie_selection
    sync_run_coroutine_function(
        EmailService.send_inactive_users_email(
            inactive_users=inactive_users,
            movie_selection=movie_selection,
        ),
    )
