from email.message import EmailMessage
from typing import Any

from aiosmtplib import SMTP
from packages.schemas.notification import (
    InactiveUser,
    InactiveUserList,
    SelectedMovieList,
)
from pydantic import EmailStr

from core.config import settings
from core.email_templates import (
    AUTH_CONFIRMATION_CODE_EMAIL_BODY_TEMPLATE,
    AUTH_CONFIRMATION_CODE_EMAIL_SUBJECT,
    EMAIL_FOOTER,
    INACTIVE_USER_EMAIL_BODY_TEMPLATE,
    INACTIVE_USER_EMAIL_SUBJECT_TEMPLATE,
    REGISTRATION_CONFIRMATION_CODE_EMAIL_BODY_TEMPLATE,
    REGISTRATION_CONFIRMATION_CODE_EMAIL_SUBJECT,
    RESET_PASSWORD_CONFIRMATION_CODE_EMAIL_BODY_TEMPLATE,
    RESET_PASSWORD_CONFIRMATION_CODE_EMAIL_SUBJECT,
    SELECTED_MOVIE_TEMPLATE,
    WELCOME_EMAIL_BODY_TEMPLATE,
    WELCOME_EMAIL_SUBJECT,
)


class EmailService:
    @staticmethod
    def get_smtp_client() -> SMTP:
        smtp_client = SMTP(
            hostname=settings.mail_host,
            port=settings.mail_port,
            username=settings.corporate_email,
            password=settings.corporate_email_password,
            start_tls=settings.start_tls,
        )
        return smtp_client

    @classmethod
    async def send_email(
        cls,
        subject: str,
        body: str,
        to_email: EmailStr,
    ) -> None:
        smtp_client = cls.get_smtp_client()
        body_with_footer = cls.add_footer(body=body, footer=EMAIL_FOOTER)
        async with smtp_client:
            message = EmailMessage()
            message["Subject"] = subject
            message["From"] = settings.corporate_email
            message["To"] = to_email
            message.set_content(body_with_footer)

            await smtp_client.send_message(
                message,
                sender=settings.corporate_email,
                recipients=[to_email],
            )

    @classmethod
    def add_footer(cls, body: str, footer: str = EMAIL_FOOTER) -> str:
        body_with_footer_list = [body, footer]
        body_with_footer = "\n".join(body_with_footer_list)
        return body_with_footer

    @classmethod
    async def send_welcome_email(cls, email: str, name: str) -> None:
        await cls.send_email(
            subject=WELCOME_EMAIL_SUBJECT,
            body=WELCOME_EMAIL_BODY_TEMPLATE.format(name=name),
            to_email=email,
        )

    @classmethod
    async def send_registration_confirmation_code_email(
        cls,
        email: EmailStr,
        confirmation_code: str,
    ) -> None:
        await cls.send_email(
            subject=REGISTRATION_CONFIRMATION_CODE_EMAIL_SUBJECT,
            body=REGISTRATION_CONFIRMATION_CODE_EMAIL_BODY_TEMPLATE.format(
                confirmation_code=confirmation_code,
            ),
            to_email=email,
        )

    @classmethod
    async def send_auth_confirmation_code_email(
        cls,
        email: EmailStr,
        confirmation_code: str,
    ) -> None:
        await cls.send_email(
            subject=AUTH_CONFIRMATION_CODE_EMAIL_SUBJECT,
            body=AUTH_CONFIRMATION_CODE_EMAIL_BODY_TEMPLATE.format(
                confirmation_code=confirmation_code,
            ),
            to_email=email,
        )

    @classmethod
    async def send_reset_password_confirmation_code_email(
        cls,
        login: str,
        email: EmailStr,
        confirmation_code: str,
    ) -> None:
        await cls.send_email(
            subject=RESET_PASSWORD_CONFIRMATION_CODE_EMAIL_SUBJECT,
            body=RESET_PASSWORD_CONFIRMATION_CODE_EMAIL_BODY_TEMPLATE.format(
                login=login,
                confirmation_code=confirmation_code,
            ),
            to_email=email,
        )

    @classmethod
    def create_movie_selection_email(cls, movie_selection: SelectedMovieList) -> str:
        movie_selection_list = [
            SELECTED_MOVIE_TEMPLATE.format(
                name=movie.name,
                genre_name=movie.genre_name,
                rating=movie.rating,
                source_url=movie.source_url,
                release_date=movie.release_date,
            )
            for movie in movie_selection.selected_movie_list
        ]
        movie_selection_body = "\n".join(movie_selection_list)
        return movie_selection_body

    @classmethod
    async def send_inactive_user_email(
        cls,
        user: InactiveUser,
        subject_template: str,
        body_template: str,
        **kwargs: Any,
    ) -> None:
        name = kwargs["name"]
        await cls.send_email(
            subject=subject_template.format(name=name),
            body=body_template.format(name=name),
            to_email=user.email,
        )

    @classmethod
    async def send_inactive_users_email(
        cls,
        inactive_users: InactiveUserList,
        movie_selection: SelectedMovieList,
    ) -> None:
        movie_selection_body = cls.create_movie_selection_email(movie_selection)
        body_template = INACTIVE_USER_EMAIL_BODY_TEMPLATE + movie_selection_body
        for user in inactive_users.inactive_user_list:
            await cls.send_inactive_user_email(
                user,
                INACTIVE_USER_EMAIL_SUBJECT_TEMPLATE,
                body_template,
                name=user.name,
            )
