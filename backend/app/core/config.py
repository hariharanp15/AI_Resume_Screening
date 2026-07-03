from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    app_name: str = "AI Resume Screening & Interview Assistant"
    api_prefix: str = "/api"
    database_url: str = "sqlite:///./dev.db"
    jwt_secret: str = "change-me-in-production"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 120
    uploads_dir: str = "uploads"
    ai_provider: str = "local"
    openai_api_key: str | None = None
    openai_model: str = "gpt-4.1-mini"


@lru_cache
def get_settings() -> Settings:
    return Settings()
