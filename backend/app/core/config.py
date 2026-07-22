from functools import lru_cache
from urllib.parse import quote

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = Field(default="NorthBrief API", alias="APP_NAME")
    environment: str = Field(default="development", alias="ENVIRONMENT")
    api_v1_prefix: str = Field(default="/api/v1", alias="API_V1_PREFIX")
    database_url: str = Field(alias="DATABASE_URL")
    database_schema: str | None = Field(default=None, alias="DB_SCHEMA")
    jwt_secret: str = Field(default="change-me", alias="JWT_SECRET")
    jwt_expire_minutes: int = Field(default=60 * 24 * 7, alias="JWT_EXPIRE_MINUTES")
    admin_email: str = Field(default="admin@northbrief.local", alias="ADMIN_EMAIL")
    admin_password: str | None = Field(default=None, alias="ADMIN_PASSWORD")
    openai_api_key: str | None = Field(default=None, alias="OPENAI_API_KEY")
    summarization_provider: str = Field(default="mock", alias="SUMMARIZATION_PROVIDER")
    cors_origins: str = Field(default="http://localhost:3000", alias="CORS_ORIGINS")
    ingest_on_startup: bool = Field(default=False, alias="INGEST_ON_STARTUP")
    ingestion_startup_min_interval_minutes: int = Field(
        default=60, alias="INGESTION_STARTUP_MIN_INTERVAL_MINUTES", ge=1
    )

    @property
    def normalized_database_url(self) -> str:
        if self.database_url.startswith("postgresql://"):
            return self.database_url.replace("postgresql://", "postgresql+psycopg://", 1)
        return self.database_url

    @property
    def sqlalchemy_database_url(self) -> str:
        url = self.normalized_database_url
        if not self.database_schema:
            return url
        separator = "&" if "?" in url else "?"
        options = quote(f"-csearch_path={self.database_schema}", safe="")
        return f"{url}{separator}options={options}"

    @property
    def cors_origin_list(self) -> list[str]:
        return [item.strip() for item in self.cors_origins.split(",") if item.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()
