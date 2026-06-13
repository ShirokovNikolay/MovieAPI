from pathlib import Path
from typing import ClassVar

from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class MinioConfig(BaseModel):
    host: str = "localhost"
    port: int = 9000
    access_key: str = "admin"
    secret_key: str = "adminadmin"  # noqa: S105
    expires_in: int = 15 * 60
    temporary_prefix: str = "tmp/"

    @property
    def url_minio(self) -> str:
        return f"http://{self.host}:{self.port}"


class CeleryConfig(BaseModel):
    delete_temporary_file_in: int = 24 * 60 * 60


class Settings(BaseSettings):
    BASE_DIR: Path = Path(__file__).parent
    minio: MinioConfig = MinioConfig()
    celery: CeleryConfig = CeleryConfig()
    model_config: ClassVar[SettingsConfigDict] = SettingsConfigDict(
        case_sensitive=False,
        env_file=BASE_DIR / ".env",
        env_nested_delimiter="__",
    )


settings = Settings()
