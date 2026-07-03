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
    cors_origins: list[str] = ["http://localhost:5173", "http://127.0.0.1:5173"]
    uploads_dir: str = "app/uploads/resumes"
    ai_provider: str = "local"
    gemini_api_key: str | None = None
    openai_api_key: str | None = None


@lru_cache
def get_settings() -> Settings:
    return Settings()
