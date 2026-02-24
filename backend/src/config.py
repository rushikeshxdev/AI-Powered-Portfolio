"""
Configuration management using Pydantic Settings.

This module defines the application configuration loaded from environment variables.
All sensitive data (API keys, database URLs, secret keys) are loaded from .env file.
"""

import json
from typing import List, Union
from pydantic import Field, field_validator
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
    
    groq_api_key: str = Field(
        default="",
        description="Groq API key for LLM fallback"
    )
    
    database_url: str = Field(
        ...,
        description="PostgreSQL database connection URL"
    )
    
    allowed_origins: Union[List[str], str] = Field(
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
    
    @field_validator("allowed_origins", mode="before")
    @classmethod
    def parse_allowed_origins(cls, v) -> List[str]:
        """Parse ALLOWED_ORIGINS from JSON string or comma-separated list."""
        if isinstance(v, list):
            return v
        if isinstance(v, str):
            # Try to parse as JSON first
            try:
                parsed = json.loads(v)
                if isinstance(parsed, list):
                    return parsed
            except json.JSONDecodeError:
                pass
            # Fall back to comma-separated parsing
            return [origin.strip() for origin in v.split(",")]
        return v
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )


# Global settings instance
settings = Settings()
