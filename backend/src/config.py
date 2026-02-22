"""
Configuration management using Pydantic Settings.

This module defines the application configuration loaded from environment variables.
All sensitive data (API keys, database URLs, secret keys) are loaded from .env file.
"""

from typing import List
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    
    Attributes:
        openrouter_api_key: API key for OpenRouter service (required)
        database_url: PostgreSQL database connection URL (required)
        allowed_origins: List of allowed CORS origins for frontend access
        secret_key: Secret key for session management and security (required)
        environment: Application environment (development, production, etc.)
    """
    
    openrouter_api_key: str = Field(
        ...,
        description="OpenRouter API key for LLM access"
    )
    
    database_url: str = Field(
        ...,
        description="PostgreSQL database connection URL"
    )
    
    allowed_origins: List[str] = Field(
        default=["http://localhost:5173"],
        description="Allowed CORS origins for API access"
    )
    
    secret_key: str = Field(
        ...,
        description="Secret key for security operations"
    )
    
    environment: str = Field(
        default="development",
        description="Application environment (development, production, etc.)"
    )
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )


# Global settings instance
settings = Settings()
