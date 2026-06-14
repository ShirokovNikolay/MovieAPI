from pathlib import Path
from typing import ClassVar

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    BASE_DIR: Path = Path(__file__).parent.parent
    mail_host: str = "smtp.yandex.ru"
    mail_port: int = 587
    corporate_email: str = "email"
    corporate_email_password: str = "password"  # noqa: S105
    start_tls: bool = True
    model_config: ClassVar[SettingsConfigDict] = SettingsConfigDict(
        case_sensitive=False,
        env_file=BASE_DIR / ".env",
        env_nested_delimiter="__",
    )


settings = Settings()
