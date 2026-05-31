from pathlib import Path
from typing import ClassVar

from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class MinioConfig(BaseModel):
    host: str = "minio"
    port: int = 9000


class Settings(BaseSettings):
    BASE_DIR: Path = Path(__file__).parent
    minio: MinioConfig = MinioConfig()
    model_config: ClassVar[SettingsConfigDict] = SettingsConfigDict(
        case_sensitive=False,
        env_file=BASE_DIR / ".env",
        env_nested_delimiter="__",
    )
