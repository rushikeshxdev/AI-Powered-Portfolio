"""
Tests for configuration management.
"""

import pytest
from pydantic import ValidationError
from src.config import Settings


def test_settings_with_all_required_fields(monkeypatch):
    """Test that Settings loads correctly with all required fields."""
    monkeypatch.setenv("OPENROUTER_API_KEY", "test_api_key")
    monkeypatch.setenv("DATABASE_URL", "postgresql+asyncpg://user:pass@localhost/db")
    monkeypatch.setenv("SECRET_KEY", "test_secret_key")
    
    settings = Settings()
    
    assert settings.openrouter_api_key == "test_api_key"
    assert settings.database_url == "postgresql+asyncpg://user:pass@localhost/db"
    assert settings.secret_key == "test_secret_key"
    assert settings.environment == "development"  # default value
    assert settings.allowed_origins == ["http://localhost:5173"]  # default value


def test_settings_with_custom_values(monkeypatch):
    """Test that Settings loads custom values correctly."""
    monkeypatch.setenv("OPENROUTER_API_KEY", "custom_key")
    monkeypatch.setenv("DATABASE_URL", "postgresql+asyncpg://custom:pass@host/db")
    monkeypatch.setenv("SECRET_KEY", "custom_secret")
    monkeypatch.setenv("ENVIRONMENT", "production")
    monkeypatch.setenv("ALLOWED_ORIGINS", "https://example.com,https://app.example.com")
    
    settings = Settings()
    
    assert settings.openrouter_api_key == "custom_key"
    assert settings.database_url == "postgresql+asyncpg://custom:pass@host/db"
    assert settings.secret_key == "custom_secret"
    assert settings.environment == "production"
    assert settings.allowed_origins == ["https://example.com", "https://app.example.com"]


def test_settings_missing_required_field(monkeypatch):
    """Test that Settings raises ValidationError when required fields are missing."""
    monkeypatch.setenv("OPENROUTER_API_KEY", "test_key")
    # Missing DATABASE_URL and SECRET_KEY
    
    with pytest.raises(ValidationError) as exc_info:
        Settings()
    
    errors = exc_info.value.errors()
    error_fields = {error["loc"][0] for error in errors}
    assert "database_url" in error_fields
    assert "secret_key" in error_fields


def test_settings_case_insensitive(monkeypatch):
    """Test that Settings handles case-insensitive environment variables."""
    monkeypatch.setenv("openrouter_api_key", "test_key")
    monkeypatch.setenv("database_url", "postgresql+asyncpg://user:pass@localhost/db")
    monkeypatch.setenv("secret_key", "test_secret")
    
    settings = Settings()
    
    assert settings.openrouter_api_key == "test_key"
    assert settings.database_url == "postgresql+asyncpg://user:pass@localhost/db"
    assert settings.secret_key == "test_secret"


def test_allowed_origins_single_value(monkeypatch):
    """Test that allowed_origins works with a single value."""
    monkeypatch.setenv("OPENROUTER_API_KEY", "test_key")
    monkeypatch.setenv("DATABASE_URL", "postgresql+asyncpg://user:pass@localhost/db")
    monkeypatch.setenv("SECRET_KEY", "test_secret")
    monkeypatch.setenv("ALLOWED_ORIGINS", "https://example.com")
    
    settings = Settings()
    
    assert settings.allowed_origins == ["https://example.com"]
