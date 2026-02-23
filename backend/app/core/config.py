from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "FUP Marketing Analytics"
    api_v1_prefix: str = "/api/v1"
    debug: bool = True

    # Локальный режим без Docker: SQLite по умолчанию
    database_url: str = "sqlite:///./analytics.db"
    redis_url: str = "redis://localhost:6379/0"

    jwt_secret_key: str = "change-me"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 120

    demo_mode: bool = True

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


settings = Settings()
