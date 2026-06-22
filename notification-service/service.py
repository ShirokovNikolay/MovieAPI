from email.message import EmailMessage

from aiosmtplib import SMTP
from pydantic import EmailStr

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
        to_email: EmailStr,
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
        subject = "Потому что вы любите кино так же сильно, как и мы 🎬"
        # ruff: disable[W293, E501]
        body_template = """
        Дорогой {name},

        Некоторые люди смотрят фильмы. Другие — живут ими.
        
        Если вы читаете это, вам, скорее всего, важнее не просто названия и постеры. Вам важны истории.
        
        Тот самый кадр, который остаётся с вами на дни.
        
        Именно для этого мы создали MovieAPI.
        
        Представьте, что это ваш второй дом:
        
        Записывайте каждый фильм, который вы когда-либо видели
        
        Открывайте скрытые жемчужины, которые вы никогда не найдёте на популярных сайтах
        
        Ведите свой личный блокнот с мыслями и оценками
        
        Никаких алгоритмов, кричащих на вас. Только чистое кино.
        
        Добро пожаловать домой, {name}.
        
        Давайте посмотрим что-то великое.
        
        — Команда MovieAPI
        """
        # ruff: enable[W293, E501]
        await cls.send_email(
            subject=subject,
            body=body_template.format(name=name),
            to_email=email,
        )

    @classmethod
    async def send_confirm_registration_email(
        cls,
        email: EmailStr,
        confirmation_code: str,
    ) -> None:
        subject = "🔑 MovieAPI — Код подтверждения регистрации"
        # ruff: disable[W293, E501]
        body_template = """
                Здравствуйте!
                
                Спасибо за регистрацию в MovieAPI.
                
                Для завершения создания аккаунта и подтверждения вашего email-адреса,
                
                пожалуйста, введите следующий код на странице регистрации: {confirmation_code}
                
                Код действителен в течение 60 секунд.
                
                Если вы не регистрировались на нашем сайте, просто проигнорируйте это письмо.
                
                — Команда MovieAPI
                """
        # ruff: enable[W293, E501]
        await cls.send_email(
            subject=subject,
            body=body_template.format(confirmation_code=confirmation_code),
            to_email=email,
        )

    @classmethod
    async def send_confirm_login_email(
        cls,
        email: EmailStr,
        confirmation_code: str,
    ) -> None:
        subject = "🛡️ Код безопасности для входа в MovieAPI"
        # ruff: disable[W293, E501]
        body_template = """
        Здравствуйте!
        
        Выполнен запрос на вход в ваш аккаунт MovieAPI.
        
        Для подтверждения личности введите одноразовый код безопасности: {confirmation_code}
        
        Код действует 60 секунд. Никому не сообщайте этот код.
        
        Если вы не запрашивали вход в аккаунт MovieAPI, просто проигнорируйте это письмо.
        
        — Команда MovieAPI
        """
        # ruff: enable[W293, E501]
        await cls.send_email(
            subject=subject,
            body=body_template.format(confirmation_code=confirmation_code),
            to_email=email,
        )

    @classmethod
    async def send_reset_password_email_data(
        cls,
        login: str,
        email: EmailStr,
        confirmation_code: str,
    ) -> None:
        subject = "🛡️ Восстановление доступа к приложению MovieAPI"
        # ruff: disable[W293]
        body_template = """
        Здравствуйте!

        Мы получили запрос на восстановление доступа к вашему аккаунту.
        
        Ваш логин: {login}
        
        Чтобы войти, создайте новый пароль, используя код подтверждения.
        
        Ваш код подтверждения: {confirmation_code}
        
        Код подтверждения действует 60 секунд.

        Если вы не запрашивали восстановление, просто проигнорируйте это письмо.
        """
        # ruff: enable[W293]
        await cls.send_email(
            subject=subject,
            body=body_template.format(
                login=login,
                confirmation_code=confirmation_code,
            ),
            to_email=email,
        )
