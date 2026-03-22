from pathlib import Path

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


class Settings(BaseSettings):
    BASE_DIR: Path = Path(__file__).parent
    database: DataBaseConfig
    debug: bool

    model_config: SettingsConfigDict = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_nested_delimiter="__",
    )


settings = Settings()
