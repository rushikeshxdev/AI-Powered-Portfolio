"""
Security headers middleware for FastAPI application.

This module implements middleware that adds security-related HTTP headers
to all responses to protect against common web vulnerabilities.
"""

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """
    Middleware that adds security headers to all HTTP responses.
    
    This middleware adds the following security headers:
    - X-Content-Type-Options: nosniff - Prevents MIME type sniffing
    - X-Frame-Options: DENY - Prevents clickjacking attacks
    - X-XSS-Protection: 1; mode=block - Enables XSS filtering in browsers
    - Strict-Transport-Security: Enforces HTTPS connections
    - Content-Security-Policy: Restricts resource loading to same origin
    
    These headers help protect against common web vulnerabilities including
    XSS, clickjacking, MIME type confusion, and man-in-the-middle attacks.
    """
    
    async def dispatch(self, request: Request, call_next) -> Response:
        """
        Process the request and add security headers to the response.
        
        Args:
            request: The incoming HTTP request
            call_next: The next middleware or route handler in the chain
            
        Returns:
            Response with security headers added
        """
        # Call the next middleware or route handler
        response = await call_next(request)
        
        # Add security headers
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        response.headers["Content-Security-Policy"] = "default-src 'self'"
        
        return response
