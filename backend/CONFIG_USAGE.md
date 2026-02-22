# Configuration Management Usage Guide

## Overview

The `config.py` module provides centralized configuration management using Pydantic Settings. All configuration values are loaded from environment variables and the `.env` file.

## Configuration Fields

### Required Fields

1. **openrouter_api_key** (str)
   - OpenRouter API key for LLM access
   - Get your key from: https://openrouter.ai/
   - Environment variable: `OPENROUTER_API_KEY`

2. **database_url** (str)
   - PostgreSQL database connection URL
   - Format: `postgresql+asyncpg://user:password@host:port/database`
   - Environment variable: `DATABASE_URL`

3. **secret_key** (str)
   - Secret key for security operations (session management, JWT, etc.)
   - Generate using: `openssl rand -hex 32`
   - Environment variable: `SECRET_KEY`

### Optional Fields (with defaults)

4. **allowed_origins** (List[str])
   - List of allowed CORS origins for API access
   - Default: `["http://localhost:5173"]`
   - Environment variable: `ALLOWED_ORIGINS` (comma-separated)
   - Example: `http://localhost:5173,http://localhost:3000`

5. **environment** (str)
   - Application environment
   - Default: `"development"`
   - Environment variable: `ENVIRONMENT`
   - Valid values: `development`, `production`, `staging`, etc.

## Usage

### Basic Import

```python
from src.config import settings

# Access configuration values
api_key = settings.openrouter_api_key
db_url = settings.database_url
origins = settings.allowed_origins
```

### In FastAPI Application

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.config import settings

app = FastAPI()

# Configure CORS with settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Environment-Specific Configuration

```python
from src.config import settings

if settings.environment == "production":
    # Production-specific configuration
    debug = False
    log_level = "INFO"
else:
    # Development configuration
    debug = True
    log_level = "DEBUG"
```

## Setup Instructions

### 1. Create .env File

```bash
cp .env.example .env
```

### 2. Edit .env File

```bash
# Database Configuration
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/ai_portfolio

# OpenRouter API Configuration
OPENROUTER_API_KEY=your_actual_api_key_here

# CORS Configuration
ALLOWED_ORIGINS=http://localhost:5173,http://localhost:3000

# Security
SECRET_KEY=your_generated_secret_key_here

# Environment
ENVIRONMENT=development
```

### 3. Generate Secret Key

```bash
# On Linux/Mac
openssl rand -hex 32

# On Windows (PowerShell)
python -c "import secrets; print(secrets.token_hex(32))"
```

## Features

### Case-Insensitive Environment Variables

The configuration is case-insensitive, so these are equivalent:
- `OPENROUTER_API_KEY`
- `openrouter_api_key`
- `OpenRouter_API_Key`

### Automatic Type Conversion

Pydantic automatically converts environment variables to the correct types:
- Comma-separated strings → List[str] for `allowed_origins`
- String values → str for other fields

### Validation

The Settings class validates all required fields on initialization:
- Missing required fields will raise a `ValidationError`
- Invalid types will be automatically converted or raise an error
- Extra environment variables are ignored

## Error Handling

### Missing Required Fields

```python
# If OPENROUTER_API_KEY is not set
ValidationError: 1 validation error for Settings
openrouter_api_key
  field required (type=value_error.missing)
```

### Invalid Values

```python
# If DATABASE_URL is empty
ValidationError: 1 validation error for Settings
database_url
  field required (type=value_error.missing)
```

## Security Best Practices

1. **Never commit .env file** - It's already in .gitignore
2. **Use strong secret keys** - Generate with `openssl rand -hex 32`
3. **Rotate keys regularly** - Especially in production
4. **Use environment-specific .env files** - Different keys for dev/staging/prod
5. **Never log sensitive values** - API keys, database passwords, secret keys

## Testing

For testing, you can override environment variables:

```python
import pytest
from src.config import Settings

def test_settings_with_custom_values(monkeypatch):
    monkeypatch.setenv("OPENROUTER_API_KEY", "test_key")
    monkeypatch.setenv("DATABASE_URL", "postgresql+asyncpg://test:test@localhost/test")
    monkeypatch.setenv("SECRET_KEY", "test_secret")
    
    settings = Settings()
    
    assert settings.openrouter_api_key == "test_key"
    assert settings.environment == "development"  # default value
```

## Troubleshooting

### Issue: Settings not loading from .env

**Solution**: Ensure .env file is in the backend root directory (same level as src/)

### Issue: ValidationError on startup

**Solution**: Check that all required fields are set in .env file

### Issue: CORS errors in frontend

**Solution**: Verify ALLOWED_ORIGINS includes your frontend URL

## References

- [Pydantic Settings Documentation](https://docs.pydantic.dev/latest/concepts/pydantic_settings/)
- [FastAPI Configuration](https://fastapi.tiangolo.com/advanced/settings/)
- [Environment Variables Best Practices](https://12factor.net/config)
