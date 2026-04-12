from pathlib import Path

from fastapi.security import HTTPBearer, OAuth2PasswordBearer
from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class DataBaseConfig(BaseModel):
    user: str = "postgres"
    password: str = "postgres"
    host: str = "localhost"
    port: int = 5432
    db_name: str = "movie-catalog"
    echo: bool = False

    @property
    def url_database(self) -> str:
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.db_name}"


class RedisConnectionConfig(BaseModel):
    host: str = "localhost"
    port: int = 6379


class RedisDataBaseConfig(BaseModel):
    default: int = 0
    genres: int = 1
    movies: int = 2
    users: int = 3
    reviews: int = 4
    favorite_movies: int = 5
    watch_history: int = 6


class RedisConfig(BaseModel):
    connection: RedisConnectionConfig = RedisConnectionConfig()
    db: RedisDataBaseConfig = RedisDataBaseConfig()


class AuthJWTConfig(BaseModel):
    secret_key: str = "secret_key"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 15
    refresh_token_expire_minutes: int = 30 * 24 * 60


class Settings(BaseSettings):
    BASE_DIR: Path = Path(__file__).parent.parent
    database: DataBaseConfig = DataBaseConfig()
    redis: RedisConfig = RedisConfig()
    auth_jwt: AuthJWTConfig = AuthJWTConfig()
    http_bearer: HTTPBearer = HTTPBearer()
    oauth2_scheme: OAuth2PasswordBearer = OAuth2PasswordBearer("/api/v1/auth/login")
    debug: bool = False

    model_config: SettingsConfigDict = SettingsConfigDict(
        case_sensitive=False,
        env_file=BASE_DIR / ".env",
        env_nested_delimiter="__",
    )


settings = Settings()
