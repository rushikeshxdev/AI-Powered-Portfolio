"""
Structured logging configuration for AI Portfolio backend.

This module provides JSON-formatted logging with:
- Timestamp, level, logger name, message, request_id
- Stack traces for errors (exc_info)
- RotatingFileHandler with 10MB max size and 5 backups
- Console output for development
"""

import json
import logging
import os
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Optional


class JSONFormatter(logging.Formatter):
    """
    Custom JSON formatter for structured logging.
    
    Formats log records as JSON with fields:
    - timestamp: ISO 8601 formatted timestamp
    - level: Log level (INFO, ERROR, etc.)
    - logger: Logger name (module path)
    - message: Log message
    - request_id: Request ID if available (from LoggerAdapter)
    - exc_info: Stack trace if exception occurred
    """
    
    def format(self, record: logging.LogRecord) -> str:
        """
        Format log record as JSON string.
        
        Args:
            record: LogRecord instance to format
            
        Returns:
            JSON-formatted log string
        """
        # Format timestamp as ISO 8601 with milliseconds
        from datetime import datetime
        dt = datetime.fromtimestamp(record.created)
        timestamp = dt.strftime("%Y-%m-%dT%H:%M:%S") + f".{int(record.msecs):03d}Z"
        
        log_data = {
            "timestamp": timestamp,
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }
        
        # Add request_id if present (set by middleware or LoggerAdapter)
        if hasattr(record, "request_id"):
            log_data["request_id"] = record.request_id
        
        # Add exception info if present
        if record.exc_info:
            log_data["exc_info"] = self.formatException(record.exc_info)
        
        return json.dumps(log_data)


def setup_logging(
    log_level: str = "INFO",
    log_file: str = "backend/logs/app.log",
    max_bytes: int = 10 * 1024 * 1024,  # 10MB
    backup_count: int = 5,
    enable_console: bool = True
) -> None:
    """
    Configure structured logging with JSON format and rotating file handler.
    
    This function:
    1. Creates logs directory if it doesn't exist
    2. Configures RotatingFileHandler with JSON formatter
    3. Optionally adds console handler for development
    4. Sets log level from environment or parameter
    
    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Path to log file
        max_bytes: Maximum log file size before rotation (default 10MB)
        backup_count: Number of backup files to keep (default 5)
        enable_console: Whether to enable console output (default True)
    """
    # Create logs directory if it doesn't exist
    log_path = Path(log_file)
    log_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Get log level from environment or use parameter
    level_str = os.getenv("LOG_LEVEL", log_level).upper()
    level = getattr(logging, level_str, logging.INFO)
    
    # Create root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(level)
    
    # Remove existing handlers to avoid duplicates
    root_logger.handlers.clear()
    
    # Create JSON formatter
    json_formatter = JSONFormatter()
    
    # Configure rotating file handler
    file_handler = RotatingFileHandler(
        filename=log_file,
        maxBytes=max_bytes,
        backupCount=backup_count,
        encoding="utf-8"
    )
    file_handler.setLevel(level)
    file_handler.setFormatter(json_formatter)
    root_logger.addHandler(file_handler)
    
    # Configure console handler for development
    if enable_console:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(level)
        
        # Use simple format for console (more readable than JSON)
        console_formatter = logging.Formatter(
            fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        console_handler.setFormatter(console_formatter)
        root_logger.addHandler(console_handler)
    
    # Log initialization message
    root_logger.info(
        f"Logging configured: level={level_str}, file={log_file}, "
        f"max_bytes={max_bytes}, backup_count={backup_count}"
    )


def get_logger_with_request_id(name: str, request_id: Optional[str] = None) -> logging.LoggerAdapter:
    """
    Get a logger adapter that includes request_id in all log records.
    
    This is useful for adding request context to logs within request handlers.
    
    Args:
        name: Logger name (typically __name__)
        request_id: Request ID to include in logs
        
    Returns:
        LoggerAdapter that adds request_id to all log records
        
    Example:
        logger = get_logger_with_request_id(__name__, request_id="abc123")
        logger.info("Processing request")  # Will include request_id in JSON
    """
    logger = logging.getLogger(name)
    extra = {"request_id": request_id} if request_id else {}
    return logging.LoggerAdapter(logger, extra)
