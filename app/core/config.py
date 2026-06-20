from pathlib import Path
from typing import ClassVar

from fastapi.security import HTTPBearer, OAuth2PasswordBearer
from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class DataBaseConfig(BaseModel):
    user: str = "postgres"
    password: str = "postgres"
    host: str = "database"
    port: int = 5432
    db_name: str = "movie-catalog"
    echo: bool = False

    @property
    def url_database(self) -> str:
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.db_name}"


class RedisConnectionConfig(BaseModel):
    host: str = "redis"
    port: int = 6379


class RedisDataBaseConfig(BaseModel):
    rate_limiter: int = 0
    genres: int = 1
    movies: int = 2
    users: int = 3
    reviews: int = 4
    favorite_movies: int = 5
    watch_history: int = 6
    confirmation_codes: int = 7


class RedisConfig(BaseModel):
    connection: RedisConnectionConfig = RedisConnectionConfig()
    db: RedisDataBaseConfig = RedisDataBaseConfig()


class RabbitMQConfig(BaseModel):
    host: str = "rabbitmq"
    port: int = 5672
    user: str = "guest"
    password: str = "guest"

    @property
    def url_rabbitmq(self) -> str:
        return f"amqp://{self.user}:{self.password}@{self.host}:{self.port}/"


class AuthJWTConfig(BaseModel):
    secret_key: str = "secret_key"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 15
    refresh_token_expire_minutes: int = 30 * 24 * 60


class ConfirmationCodeJWTConfig(BaseModel):
    secret_key: str = "secret_key"
    algorithm: str = "HS256"
    temporary_token_registration_expire_minutes: int = 15
    temporary_token_two_factor_expire_minutes: int = 15
    temporary_token_reset_password_expire_minutes: int = 15


class MediaServiceConfig(BaseModel):
    host: str = "mediaservice"
    port: int = 8000

    @property
    def create_presign_url_endpoint(self) -> str:
        return f"http://{self.host}:{self.port}/api/v1/presign-url"


class NotificationServiceConfig(BaseModel):
    host: str = "notification-service"
    port: int = 8000

    @property
    def send_email_endpoint(self) -> str:
        return f"http://{self.host}:{self.port}/api/v1/send-email"


class Settings(BaseSettings):
    BASE_DIR: Path = Path(__file__).parent.parent
    database: DataBaseConfig = DataBaseConfig()
    redis: RedisConfig = RedisConfig()
    rabbitmq: RabbitMQConfig = RabbitMQConfig()
    auth_jwt: AuthJWTConfig = AuthJWTConfig()
    confirmation_code_jwt: ConfirmationCodeJWTConfig = ConfirmationCodeJWTConfig()
    http_bearer: HTTPBearer = HTTPBearer()
    oauth2_scheme: OAuth2PasswordBearer = OAuth2PasswordBearer(
        "/api/v1/auth/confirm-email",
    )
    media_service: MediaServiceConfig = MediaServiceConfig()
    notification_service: NotificationServiceConfig = NotificationServiceConfig()
    debug: bool = False

    model_config: ClassVar[SettingsConfigDict] = SettingsConfigDict(
        case_sensitive=False,
        env_file=BASE_DIR / ".env",
        env_nested_delimiter="__",
    )


settings = Settings()
