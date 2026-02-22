"""
Request ID middleware for tracking requests across the application.

This middleware:
1. Generates a unique request_id for each incoming request
2. Adds request_id to request.state for access in route handlers
3. Includes request_id in response headers for client-side tracking
4. Enables request_id to be included in all logs for that request
"""

import uuid
import logging
from typing import Callable

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware


logger = logging.getLogger(__name__)


class RequestIDMiddleware(BaseHTTPMiddleware):
    """
    Middleware that adds a unique request_id to each request.
    
    The request_id is:
    - Generated as a UUID4 if not provided in X-Request-ID header
    - Stored in request.state.request_id for access in handlers
    - Added to response headers as X-Request-ID
    - Available for logging throughout the request lifecycle
    """
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """
        Process request and add request_id.
        
        Args:
            request: Incoming FastAPI request
            call_next: Next middleware or route handler
            
        Returns:
            Response with X-Request-ID header
        """
        # Check if client provided request_id in header
        request_id = request.headers.get("X-Request-ID")
        
        # Generate new request_id if not provided
        if not request_id:
            request_id = str(uuid.uuid4())
        
        # Store request_id in request state for access in handlers
        request.state.request_id = request_id
        
        # Log request with request_id
        logger.info(
            f"Request started: {request.method} {request.url.path}",
            extra={"request_id": request_id}
        )
        
        # Process request
        try:
            response = await call_next(request)
            
            # Add request_id to response headers
            response.headers["X-Request-ID"] = request_id
            
            # Log response with request_id
            logger.info(
                f"Request completed: {request.method} {request.url.path} - "
                f"Status: {response.status_code}",
                extra={"request_id": request_id}
            )
            
            return response
            
        except Exception as e:
            # Log error with request_id and stack trace
            logger.error(
                f"Request failed: {request.method} {request.url.path} - Error: {str(e)}",
                exc_info=True,
                extra={"request_id": request_id}
            )
            raise
