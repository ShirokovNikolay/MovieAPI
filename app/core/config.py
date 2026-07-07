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
    def url(self) -> str:
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
    auth: int = 7
    celery_backend: int = 8
    cache_versioning: int = 9


class RedisConfig(BaseModel):
    connection: RedisConnectionConfig = RedisConnectionConfig()
    db: RedisDataBaseConfig = RedisDataBaseConfig()


class RabbitMQConfig(BaseModel):
    host: str = "rabbitmq"
    port: int = 5672
    user: str = "guest"
    password: str = "guest"

    @property
    def url(self) -> str:
        return f"amqp://{self.user}:{self.password}@{self.host}:{self.port}/"


class AuthJWTConfig(BaseModel):
    secret_key: str = "secret_key"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 15
    refresh_token_expire_minutes: int = 30 * 24 * 60


class RegistrationJWTConfig(BaseModel):
    secret_key: str = "secret_key"
    algorithm: str = "HS256"
    expire_minutes: int = 15


class TwoFactorJWTConfig(BaseModel):
    secret_key: str = "secret_key"
    algorithm: str = "HS256"
    expire_minutes: int = 15


class RecoverJWTConfig(BaseModel):
    secret_key: str = "secret_key"
    algorithm: str = "HS256"
    expire_minutes: int = 15


class ResetPasswordJWTConfig(BaseModel):
    secret_key: str = "secret_key"
    algorithm: str = "HS256"
    expire_minutes: int = 15


class JWTConfig(BaseModel):
    auth: AuthJWTConfig = AuthJWTConfig()
    registration: RegistrationJWTConfig = RegistrationJWTConfig()
    two_factor_auth: TwoFactorJWTConfig = TwoFactorJWTConfig()
    recover: RecoverJWTConfig = RecoverJWTConfig()
    reset_password: ResetPasswordJWTConfig = ResetPasswordJWTConfig()


class ScheduleConfig(BaseModel):
    minute: str | int = "*"
    hour: str | int = "*"
    day_of_week: str | int = "*"
    day_of_month: str | int = "*"
    month_of_year: str | int = "*"


class CeleryBeatConfig(BaseModel):
    notify_inactive_users_with_movie_picks: ScheduleConfig = ScheduleConfig(
        day_of_week="sun",
        hour=16,
        minute=0,
    )


class CeleryConfig(BaseModel):
    beat: CeleryBeatConfig = CeleryBeatConfig()
    base_dir: Path = Path(__file__).parent.parent / ".core" / "celery" / "celery_app"


class MediaServiceConfig(BaseModel):
    host: str = "media-service"
    port: int = 8000

    @property
    def create_presign_url_endpoint(self) -> str:
        return f"http://{self.host}:{self.port}/api/v1/presign-url"


class NotificationServiceConfig(BaseModel):
    host: str = "notification-service"
    port: int = 8000


class Settings(BaseSettings):
    service_name: str = "movie-catalog"
    base_dir: Path = Path(__file__).parent.parent
    database: DataBaseConfig = DataBaseConfig()
    redis: RedisConfig = RedisConfig()
    rabbitmq: RabbitMQConfig = RabbitMQConfig()
    jwt: JWTConfig = JWTConfig()
    celery: CeleryConfig = CeleryConfig()
    http_bearer: HTTPBearer = HTTPBearer()
    oauth2_scheme: OAuth2PasswordBearer = OAuth2PasswordBearer(
        "/api/v1/auth/login/",
    )
    media_service: MediaServiceConfig = MediaServiceConfig()
    notification_service: NotificationServiceConfig = NotificationServiceConfig()
    debug: bool = False

    model_config: ClassVar[SettingsConfigDict] = SettingsConfigDict(
        case_sensitive=False,
        env_file=base_dir / ".env",
        env_nested_delimiter="__",
    )


settings = Settings()
