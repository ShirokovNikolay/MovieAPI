from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    debug: bool = True
    model_config: SettingsConfigDict = SettingsConfigDict(
        env_file="./env",
    )


settings = Settings()
