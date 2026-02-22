# Structured Logging Implementation

This document describes the structured logging implementation for the AI Portfolio backend.

## Overview

The application uses structured JSON logging with the following features:
- **JSON Format**: All logs are written in JSON format for easy parsing and analysis
- **Rotating File Handler**: Logs rotate at 10MB with 5 backup files
- **Request ID Tracking**: Each request gets a unique ID that's included in all logs
- **Stack Traces**: All errors include full stack traces in the `exc_info` field
- **Console Output**: Development mode includes human-readable console output

## Components

### 1. Logging Configuration (`src/logging_config.py`)

#### JSONFormatter
Custom formatter that outputs logs in JSON format with the following fields:
- `timestamp`: ISO 8601 formatted timestamp (e.g., "2024-01-01T10:00:00.123Z")
- `level`: Log level (INFO, WARNING, ERROR, etc.)
- `logger`: Logger name (module path)
- `message`: Log message
- `request_id`: Request ID (if available)
- `exc_info`: Stack trace (if exception occurred)

#### setup_logging()
Configures the logging system with:
- RotatingFileHandler: 10MB max size, 5 backups
- Log file location: `backend/logs/app.log`
- Console handler for development (optional)
- Configurable log level via `LOG_LEVEL` environment variable

#### get_logger_with_request_id()
Helper function to create a logger adapter that includes request_id in all log records.

### 2. Request ID Middleware (`src/middleware/request_id.py`)

#### RequestIDMiddleware
Middleware that:
1. Generates a unique UUID4 for each request (or uses X-Request-ID header if provided)
2. Stores request_id in `request.state.request_id`
3. Adds X-Request-ID header to all responses
4. Logs request start and completion with request_id

### 3. Main Application Updates (`src/main.py`)

All logging statements have been updated to include request_id:
- Rate limit violations
- Validation errors
- General exceptions
- Chat endpoint operations
- Database operations
- RAG engine operations

## Usage

### Application Startup

The logging system is automatically configured when the application starts:

```python
from src.logging_config import setup_logging

# Configure logging on startup
setup_logging(
    log_level="INFO",
    log_file="backend/logs/app.log",
    max_bytes=10 * 1024 * 1024,  # 10MB
    backup_count=5,
    enable_console=True
)
```

### Logging in Route Handlers

Access the request_id from request.state:

```python
@app.get("/api/example")
async def example_endpoint(request: Request):
    request_id = getattr(request.state, "request_id", "unknown")
    
    logger.info(
        "Processing example request",
        extra={"request_id": request_id}
    )
    
    try:
        # Your code here
        pass
    except Exception as e:
        logger.error(
            f"Error in example endpoint: {e}",
            exc_info=True,
            extra={"request_id": request_id}
        )
        raise
```

### Logging with Request ID Adapter

For more complex operations, use the logger adapter:

```python
from src.logging_config import get_logger_with_request_id

def process_data(request_id: str):
    logger = get_logger_with_request_id(__name__, request_id)
    
    logger.info("Starting data processing")
    # request_id is automatically included in all logs
    
    try:
        # Your code here
        logger.info("Data processing completed")
    except Exception as e:
        logger.error(f"Processing failed: {e}", exc_info=True)
```

## Log Format Examples

### Standard Log Entry
```json
{
  "timestamp": "2024-01-01T10:00:00.123Z",
  "level": "INFO",
  "logger": "src.main",
  "message": "Chat request from IP 192.168.1.1, session abc123",
  "request_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

### Error Log with Stack Trace
```json
{
  "timestamp": "2024-01-01T10:00:05.456Z",
  "level": "ERROR",
  "logger": "src.main",
  "message": "Database error while storing message: connection timeout",
  "request_id": "550e8400-e29b-41d4-a716-446655440000",
  "exc_info": "Traceback (most recent call last):\n  File \"src/main.py\", line 123, in generate_sse_stream\n    await chat_repo.save_message(...)\nSQLAlchemyError: connection timeout"
}
```

### Rate Limit Violation
```json
{
  "timestamp": "2024-01-01T10:00:10.789Z",
  "level": "WARNING",
  "logger": "src.main",
  "message": "Rate limit exceeded - IP: 192.168.1.1, Path: /api/chat, Timestamp: 2024-01-01T10:00:10.789Z",
  "request_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

## Log File Management

### Rotation
- Logs automatically rotate when they reach 10MB
- Up to 5 backup files are kept (app.log.1, app.log.2, etc.)
- Oldest backups are deleted when the limit is reached

### Location
- Primary log file: `backend/logs/app.log`
- Backup files: `backend/logs/app.log.1` through `app.log.5`

### Viewing Logs

#### View recent logs (console)
```bash
tail -f backend/logs/app.log
```

#### Parse JSON logs with jq
```bash
# View all logs
cat backend/logs/app.log | jq '.'

# Filter by level
cat backend/logs/app.log | jq 'select(.level == "ERROR")'

# Filter by request_id
cat backend/logs/app.log | jq 'select(.request_id == "550e8400-e29b-41d4-a716-446655440000")'

# View only error messages
cat backend/logs/app.log | jq 'select(.level == "ERROR") | .message'
```

## Configuration

### Environment Variables

- `LOG_LEVEL`: Set log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
  - Default: INFO
  - Example: `LOG_LEVEL=DEBUG`

### Customization

To customize logging behavior, modify `src/logging_config.py`:

```python
setup_logging(
    log_level="DEBUG",              # More verbose logging
    log_file="logs/custom.log",     # Different log file
    max_bytes=50 * 1024 * 1024,     # 50MB max size
    backup_count=10,                # Keep 10 backups
    enable_console=False            # Disable console output
)
```

## Testing

### Manual Test
Run the manual test to verify logging configuration:

```bash
cd backend
python test_logging_manual.py
```

This test verifies:
- JSON formatting
- Request ID inclusion
- Stack trace logging
- File rotation configuration

### Integration Test
Run the integration test to verify logging with FastAPI:

```bash
cd backend
python test_logging_integration.py
```

This test verifies:
- Logging works with FastAPI application
- Request ID middleware adds headers
- Logs are written in JSON format

## Requirements Validation

This implementation satisfies the following requirements:

### Requirement 9.5: Error Handling and Resilience
- ✓ All errors logged with timestamps, request IDs, and stack traces
- ✓ Structured logging enables easy error analysis

### Requirement 14.1: Analytics and Monitoring
- ✓ All chat questions logged with timestamps
- ✓ Request tracking via request_id

### Requirement 14.2: Analytics and Monitoring
- ✓ Response times can be calculated from request start/completion logs
- ✓ All API requests logged with timing information

### Requirement 14.4: Analytics and Monitoring
- ✓ Error rates and types logged with structured format
- ✓ Easy to query and analyze error patterns

## Best Practices

1. **Always include request_id**: Use `extra={"request_id": request_id}` in all log statements
2. **Use exc_info=True for errors**: Ensures stack traces are captured
3. **Log at appropriate levels**:
   - DEBUG: Detailed diagnostic information
   - INFO: General informational messages
   - WARNING: Warning messages (e.g., rate limits, degraded mode)
   - ERROR: Error messages with stack traces
   - CRITICAL: Critical errors requiring immediate attention
4. **Keep messages concise**: The message field should be brief and descriptive
5. **Use structured data**: Include relevant context in the message or as separate fields

## Troubleshooting

### Logs not appearing
- Check that `backend/logs/` directory exists
- Verify LOG_LEVEL environment variable is set correctly
- Check file permissions on log directory

### JSON parsing errors
- Ensure all log statements use the configured logger
- Verify no direct print statements are writing to log files
- Check that custom formatters are not interfering

### Request ID not appearing
- Verify RequestIDMiddleware is added to the application
- Check that middleware is added before other middleware
- Ensure request.state.request_id is accessed correctly

## Future Enhancements

Potential improvements for the logging system:
1. **Log aggregation**: Send logs to centralized logging service (e.g., ELK, Datadog)
2. **Metrics extraction**: Extract metrics from logs for monitoring dashboards
3. **Alert integration**: Trigger alerts based on error patterns
4. **Performance logging**: Add detailed performance metrics for slow operations
5. **User action tracking**: Log user interactions for analytics
