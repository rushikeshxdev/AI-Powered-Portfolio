# Error Handling Implementation

## Overview

This document describes the comprehensive error handling implementation for the AI Portfolio backend API, covering all error scenarios specified in Requirements 9.1, 9.2, 9.3, and 9.7.

## Global Exception Handlers

### 1. ValidationError Handler (HTTP 422)

**Location**: `backend/src/main.py`

Handles Pydantic validation errors from request body parsing.

```python
@app.exception_handler(ValidationError)
async def validation_exception_handler(request: Request, exc: ValidationError):
    """Returns HTTP 422 with validation error details."""
```

**Response Format**:
```json
{
  "error": "validation_error",
  "detail": "<validation error message>"
}
```

### 2. General Exception Handler (HTTP 500)

**Location**: `backend/src/main.py`

Catches all unhandled exceptions and returns a generic error message.

```python
@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Returns HTTP 500 with generic error message."""
```

**Response Format**:
```json
{
  "error": "internal_server_error",
  "detail": "An unexpected error occurred. Please try again later."
}
```

**Features**:
- Logs full stack trace for debugging
- Returns generic message to avoid exposing internal details
- Prevents application crashes

### 3. RateLimitExceeded Handler (HTTP 429)

**Location**: `backend/src/main.py`

Handles rate limit violations (10 requests per minute per IP).

```python
@app.exception_handler(RateLimitExceeded)
async def custom_rate_limit_handler(request: Request, exc: RateLimitExceeded):
    """Returns HTTP 429 with Retry-After header."""
```

**Response Format**:
```json
{
  "error": "rate_limit_exceeded",
  "detail": "Too many requests. Please try again later."
}
```

**Headers**:
- `Retry-After: 60` (seconds)

## Service-Specific Error Handling

### 1. Database Failures (Degraded Mode)

**Location**: `backend/src/main.py` - `generate_sse_stream()`

**Behavior**:
- Catches `SQLAlchemyError` exceptions
- Logs error with full context
- Continues serving chat requests without persistence
- Sets `db_available = False` flag
- Rolls back failed transactions

**User Impact**:
- Chat functionality continues to work
- Responses are generated normally
- Chat history is not saved (temporary degraded mode)

**Example**:
```python
try:
    await chat_repo.save_message(...)
    await db_session.commit()
except SQLAlchemyError as e:
    logger.error(f"Database error: {e}", exc_info=True)
    db_available = False
    await db_session.rollback()
    # Continue in degraded mode
```

### 2. OpenRouter API Failures (HTTP 503)

**Location**: `backend/src/main.py` - `generate_sse_stream()`

**Behavior**:
- Catches `httpx.HTTPError` exceptions
- Returns user-friendly error message via SSE
- Logs error with full context

**SSE Error Response**:
```json
{
  "type": "error",
  "content": "AI service temporarily unavailable. Please try again in a moment."
}
```

**Note**: OpenRouter client already implements retry logic with exponential backoff (3 attempts: 1s, 2s, 4s delays).

### 3. Vector Store Failures (Fallback)

**Location**: `backend/src/main.py` - `generate_sse_stream()`

**Behavior**:
- Detects ChromaDB/vector store errors by checking error message
- Returns appropriate error message via SSE
- Logs error with full context

**SSE Error Response**:
```json
{
  "type": "error",
  "content": "Unable to retrieve context from knowledge base. Please try again."
}
```

**Future Enhancement**: Could fallback to direct LLM query without context retrieval.

### 4. RAG Engine Not Initialized (HTTP 503)

**Location**: `backend/src/main.py` - `chat_endpoint()`

**Behavior**:
- Checks if RAG engine exists in `app.state`
- Returns HTTP 503 if not initialized
- Prevents requests from failing with unclear errors

**Response**:
```json
{
  "detail": "AI service is not available. Please try again later."
}
```

## HTTP Status Codes

The implementation uses appropriate HTTP status codes for all error conditions:

| Status Code | Error Type | Description |
|-------------|------------|-------------|
| 400 | Bad Request | Invalid request format (handled by FastAPI) |
| 401 | Unauthorized | Authentication failure (not yet implemented) |
| 404 | Not Found | Resource not found (handled by FastAPI) |
| 422 | Unprocessable Entity | Validation errors (Pydantic) |
| 429 | Too Many Requests | Rate limit exceeded |
| 500 | Internal Server Error | Unexpected errors |
| 503 | Service Unavailable | RAG engine not initialized, OpenRouter API down |

## Error Response Schema

All error responses follow the `ErrorResponse` schema defined in `backend/src/schemas.py`:

```python
class ErrorResponse(BaseModel):
    error: str  # Error type/code
    detail: Optional[str]  # Detailed error message
    status_code: int  # HTTP status code
```

## Logging Strategy

All errors are logged with appropriate context:

```python
logger.error(
    f"Error description: {error}",
    exc_info=True  # Include stack trace
)
```

**Log Levels**:
- `ERROR`: Service failures, exceptions
- `WARNING`: Degraded mode, rate limit violations
- `INFO`: Normal operations, request processing

## Testing

### Unit Tests

Location: `backend/tests/test_error_handling.py`

Tests cover:
- Global exception handlers
- Database failure handling (degraded mode)
- OpenRouter API failure handling
- Vector store failure handling
- HTTP status code correctness
- Error response format

### Manual Verification

Location: `backend/test_error_handling_manual.py`

Verifies:
- Exception handlers are registered
- Error handling logic is present
- Error responses follow schema
- HTTP status codes are correct

Run with:
```bash
cd backend
python test_error_handling_manual.py
```

## Requirements Coverage

| Requirement | Implementation | Status |
|-------------|----------------|--------|
| 9.1 - OpenRouter failure handling | `generate_sse_stream()` catches `httpx.HTTPError` | ✓ |
| 9.2 - Vector store failure handling | `generate_sse_stream()` detects ChromaDB errors | ✓ |
| 9.3 - Database failure handling | `generate_sse_stream()` catches `SQLAlchemyError`, degraded mode | ✓ |
| 9.7 - HTTP status codes | Global handlers return 422, 429, 500, 503 | ✓ |

## Future Enhancements

1. **Vector Store Fallback**: Implement direct LLM query without context when vector store fails
2. **Circuit Breaker**: Add circuit breaker pattern for external service calls
3. **Retry Configuration**: Make retry attempts and delays configurable
4. **Error Metrics**: Track error rates and types for monitoring
5. **User Notifications**: Add frontend notifications for degraded mode
