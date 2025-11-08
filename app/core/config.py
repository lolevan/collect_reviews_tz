from functools import lru_cache
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application configuration loaded from environment variables."""

    app_name: str = Field(default="Collect Reviews", description="Имя приложения")
    app_version: str = Field(default="1.0.0", description="Версия API")
    database_url: str = Field(
        ..., description="Строка подключения к базе данных PostgreSQL"
    )
    database_echo: bool = Field(
        default=False,
        description="Флаг логирования SQL-запросов SQLAlchemy",
    )
    test_database_url: str | None = Field(
        default=None,
        description="URL тестовой базы данных (используется в pytest)",
    )
    run_migrations_on_startup: bool = Field(
        default=True,
        description="Автоматически применять миграции при старте приложения",
    )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_prefix="",
        case_sensitive=False,
    )


@lru_cache()
def get_settings() -> Settings:
    return Settings()  # type: ignore[arg-type]


settings = get_settings()
