"""
Application configuration.

Settings are loaded from environment variables (see .env.example). Nothing
secret is hard-coded here — this file only defines shape, defaults, and
validation for configuration values.
"""
from dotenv import load_dotenv
import os
from functools import lru_cache
from typing import Literal

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

# --- Load .env file explicitly ---
load_dotenv(dotenv_path="C:/Users/user/Downloads/healthvault-ai-fullstack/healthvault-ai/backend/.env")


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    # --- General ---
    PROJECT_NAME: str = "HealthVault AI API"
    ENVIRONMENT: Literal["local", "staging", "production"] = "local"
    API_V1_PREFIX: str = "/api/v1"
    DEBUG: bool = True

    # --- CORS ---
    BACKEND_CORS_ORIGINS: list[str] = ["http://localhost:3000"]

    # --- Database ---
    DATABASE_URL: str = Field(
        default=os.getenv("DATABASE_URL")  # now reads from .env
    )
    DB_POOL_SIZE: int = 10
    DB_MAX_OVERFLOW: int = 20
    DB_ECHO: bool = False

    # --- JWT Auth ---
    JWT_SECRET_KEY: str = Field(default="CHANGE_ME_IN_PRODUCTION_use_openssl_rand_hex_32")
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # --- File storage ---
    STORAGE_BACKEND: Literal["local", "azure"] = "local"
    LOCAL_STORAGE_PATH: str = "./uploads"
    MAX_UPLOAD_SIZE_MB: int = 25
    ALLOWED_UPLOAD_EXTENSIONS: list[str] = [".pdf", ".jpg", ".jpeg", ".png"]

    # --- Azure Blob Storage ---
    AZURE_STORAGE_CONNECTION_STRING: str | None = None
    AZURE_STORAGE_ACCOUNT_URL: str | None = None
    AZURE_STORAGE_CONTAINER_NAME: str = "medical-records"

    # --- Azure OpenAI ---
    AI_PROVIDER: Literal["azure", "openai", "mock"] = "mock"
    AZURE_OPENAI_ENDPOINT: str | None = None
    AZURE_OPENAI_API_KEY: str | None = None
    AZURE_OPENAI_API_VERSION: str = "2024-08-01-preview"
    AZURE_OPENAI_CHAT_DEPLOYMENT: str = "gpt-4o"
    AZURE_OPENAI_EMBEDDING_DEPLOYMENT: str = "text-embedding-3-small"
    EMBEDDING_DIMENSIONS: int = 1536

    # --- Azure Document Intelligence ---
    DOCUMENT_INTELLIGENCE_ENABLED: bool = False
    AZURE_DOCINTEL_ENDPOINT: str | None = None
    AZURE_DOCINTEL_API_KEY: str | None = None

    # --- HIPAA / audit ---
    AUDIT_LOG_ENABLED: bool = True
    SESSION_IDLE_TIMEOUT_MINUTES: int = 15

    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    @classmethod
    def _split_cors(cls, v):
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(",")]
        return v


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
