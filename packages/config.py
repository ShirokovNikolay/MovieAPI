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


class RedisConfig(BaseModel):
    host: str = "redis"
    port: int = 6379
    celery_backend_database: int = 8

    @property
    def url(self) -> str:
        return f"redis://{self.host}:{self.port}/{self.celery_backend_database}"


class Settings(BaseSettings):
    base_dir: Path = Path(__file__).parent
    rabbitmq: RabbitMQConfig = RabbitMQConfig()
    redis: RedisConfig = RedisConfig()

    model_config: ClassVar[SettingsConfigDict] = SettingsConfigDict(
        case_sensitive=False,
        env_file=base_dir / ".env",
        env_nested_delimiter="__",
    )


settings = Settings()
