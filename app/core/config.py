from pathlib import Path

from fastapi.security import HTTPBearer, OAuth2PasswordBearer
from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class DataBaseConfig(BaseModel):
    user: str
    password: str
    host: str = "localhost"
    port: int = 5432
    db_name: str
    echo: bool = False

    @property
    def url_database(self) -> str:
        return f"postgresql+psycopg://{self.user}:{self.password}@{self.host}:{self.port}/{self.db_name}"


class AuthJWTConfig(BaseModel):
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 15
    refresh_token_expire_minutes: int = 30 * 24 * 60


class Settings(BaseSettings):
    BASE_DIR: Path = Path(__file__).parent.parent
    database: DataBaseConfig
    auth_jwt: AuthJWTConfig
    http_bearer: HTTPBearer = HTTPBearer()
    oauth2_scheme: OAuth2PasswordBearer = OAuth2PasswordBearer("/api/v1/auth/login")
    debug: bool

    model_config: SettingsConfigDict = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_nested_delimiter="__",
        case_sensitive=False,
    )


settings = Settings()
