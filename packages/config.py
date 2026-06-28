from pathlib import Path
from typing import ClassVar

from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class RabbitMQConfig(BaseModel):
    host: str = "rabbitmq"
    port: int = 5672
    username: str = "guest"
    password: str = "guest"  # noqa: S105

    @property
    def url(self) -> str:
        return f"amqp://{self.username}:{self.password}@{self.host}:{self.port}/%2f"


class Settings(BaseSettings):
    BASE_DIR: Path = Path(__file__).parent
    rabbitmq: RabbitMQConfig = RabbitMQConfig()

    model_config: ClassVar[SettingsConfigDict] = SettingsConfigDict(
        case_sensitive=False,
        env_file=BASE_DIR / ".env",
        env_nested_delimiter="__",
    )


settings = Settings()
