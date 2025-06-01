from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    auth_db_url: str
    auth_db_user: str
    auth_db_password: str
    auth_db: str
    auth_db_port: int
    gateway_service_port: int
    app_name: str = "auth-service"

    model_config = SettingsConfigDict(
        env_file=Path(__file__).parent / ".env"
    )



settings = Settings()
