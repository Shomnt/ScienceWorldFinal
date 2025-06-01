from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    article_db_url: str
    article_db_user: str
    article_db_password: str
    article_db: str
    article_db_port: int
    gateway_service_port: int
    app_name: str = "article-service"

    model_config = SettingsConfigDict(
        env_file=Path(__file__).parent / ".env"
    )


settings = Settings()
