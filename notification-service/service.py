from email.message import EmailMessage

from aiosmtplib import SMTP

from core.config import settings


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
        to_email: str,
    ) -> None:
        smtp_client = cls.get_smtp_client()
        async with smtp_client:
            message = EmailMessage()
            message["Subject"] = subject
            message["From"] = settings.corporate_email
            message["To"] = to_email
            message.set_content(body)

            await smtp_client.send_message(
                message,
                sender=settings.corporate_email,
                recipients=[to_email],
            )

    @classmethod
    async def send_welcome_email(cls, email: str, name: str) -> None:
        subject = "Because you love movies as much as we do 🎬"
        # ruff: disable[W291, W293, E501]
        body_template = """
        Dear {name},
        
        Some people watch movies. Others live them.
        
        If you're reading this, you probably care about more than just titles and posters. You care about stories. 
        
        That one shot that stays with you for days.
        
        That's why we built MovieAPI.
        
        Think of it as your second home:
        
        Log every film you've ever seen
        
        Discover hidden gems you'd never find on mainstream sites
        
        Keep your own private notebook of thoughts and ratings
        
        No algorithms shouting at you. Just pure cinema.
        
        Welcome home, {name}.
        
        Let's watch something great.
        
        — The MovieAPI Team 
        """
        # ruff: enable[W291, W293, E501]
        await cls.send_email(
            subject=subject,
            body=body_template.format(name=name),
            to_email=email,
        )
