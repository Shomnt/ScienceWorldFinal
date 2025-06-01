from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    discussion_db_url: str
    discussion_db_user: str
    discussion_db_password: str
    discussion_db: str
    discussion_db_port: int
    gateway_service_port: int
    app_name: str = "discussion-service"

    model_config = SettingsConfigDict(
        env_file=Path(__file__).parent / ".env"
    )



settings = Settings()
