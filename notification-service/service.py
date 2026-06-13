from email.message import EmailMessage

from aiosmtplib import SMTP

from core.config import settings


class EmailService:
    @staticmethod
    def get_smtp_client() -> SMTP:
        smtp_client = SMTP(
            hostname=settings.mail_host,
            port=settings.mail_port,
            username=settings.corporate_mail,
            password=settings.mail_password,
            start_tls=settings.start_tls,
        )
        return smtp_client

    @classmethod
    async def send_email(
        cls,
        subject: str,
        body: str,
        from_email: str = settings.corporate_mail,
        to_email: str = settings.corporate_mail,
    ) -> None:
        smtp_client = cls.get_smtp_client()
        async with smtp_client:
            message = EmailMessage()
            message["From"] = from_email
            message["To"] = to_email
            message["Subject"] = subject
            message.set_content(body)

            await smtp_client.send_message(
                message,
                sender=from_email,
                recipients=[to_email],
            )
