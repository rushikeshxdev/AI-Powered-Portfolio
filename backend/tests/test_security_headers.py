"""
Tests for security headers middleware.

This module tests that all required security headers are present in API responses
and that the TrustedHostMiddleware properly validates Host headers.
"""

import pytest
from fastapi.testclient import TestClient
from src.main import app


@pytest.fixture
def client():
    """Create a test client for the FastAPI application."""
    return TestClient(app)


class TestSecurityHeaders:
    """Test suite for security headers middleware."""
    
    def test_security_headers_on_root_endpoint(self, client):
        """Test that security headers are present on the root endpoint."""
        response = client.get("/")
        
        # Verify all required security headers are present
        assert response.headers["X-Content-Type-Options"] == "nosniff"
        assert response.headers["X-Frame-Options"] == "DENY"
        assert response.headers["X-XSS-Protection"] == "1; mode=block"
        assert response.headers["Strict-Transport-Security"] == "max-age=31536000; includeSubDomains"
        assert response.headers["Content-Security-Policy"] == "default-src 'self'"
    
    def test_security_headers_on_health_endpoint(self, client):
        """Test that security headers are present on the health check endpoint."""
        response = client.get("/health")
        
        # Verify all required security headers are present
        assert response.headers["X-Content-Type-Options"] == "nosniff"
        assert response.headers["X-Frame-Options"] == "DENY"
        assert response.headers["X-XSS-Protection"] == "1; mode=block"
        assert response.headers["Strict-Transport-Security"] == "max-age=31536000; includeSubDomains"
        assert response.headers["Content-Security-Policy"] == "default-src 'self'"
    
    def test_security_headers_on_404_response(self, client):
        """Test that security headers are present even on 404 responses."""
        response = client.get("/nonexistent-endpoint")
        
        # Verify security headers are present even for error responses
        assert response.headers["X-Content-Type-Options"] == "nosniff"
        assert response.headers["X-Frame-Options"] == "DENY"
        assert response.headers["X-XSS-Protection"] == "1; mode=block"
        assert response.headers["Strict-Transport-Security"] == "max-age=31536000; includeSubDomains"
        assert response.headers["Content-Security-Policy"] == "default-src 'self'"
    
    def test_x_content_type_options_prevents_mime_sniffing(self, client):
        """Test that X-Content-Type-Options header is set to nosniff."""
        response = client.get("/")
        assert response.headers["X-Content-Type-Options"] == "nosniff"
    
    def test_x_frame_options_prevents_clickjacking(self, client):
        """Test that X-Frame-Options header is set to DENY."""
        response = client.get("/")
        assert response.headers["X-Frame-Options"] == "DENY"
    
    def test_x_xss_protection_enabled(self, client):
        """Test that X-XSS-Protection header is enabled with blocking mode."""
        response = client.get("/")
        assert response.headers["X-XSS-Protection"] == "1; mode=block"
    
    def test_strict_transport_security_enforces_https(self, client):
        """Test that Strict-Transport-Security header enforces HTTPS."""
        response = client.get("/")
        hsts_header = response.headers["Strict-Transport-Security"]
        
        # Verify HSTS is configured for 1 year (31536000 seconds)
        assert "max-age=31536000" in hsts_header
        # Verify includeSubDomains is set
        assert "includeSubDomains" in hsts_header
    
    def test_content_security_policy_restricts_resources(self, client):
        """Test that Content-Security-Policy header restricts resource loading."""
        response = client.get("/")
        csp_header = response.headers["Content-Security-Policy"]
        
        # Verify CSP restricts to same origin
        assert "default-src 'self'" in csp_header
    
    def test_security_headers_on_all_endpoints(self, client):
        """Test that security headers are present on multiple endpoints."""
        endpoints = ["/", "/health"]
        
        for endpoint in endpoints:
            response = client.get(endpoint)
            
            # Verify all security headers are present
            assert "X-Content-Type-Options" in response.headers
            assert "X-Frame-Options" in response.headers
            assert "X-XSS-Protection" in response.headers
            assert "Strict-Transport-Security" in response.headers
            assert "Content-Security-Policy" in response.headers


class TestTrustedHostMiddleware:
    """Test suite for TrustedHostMiddleware."""
    
    def test_localhost_is_allowed(self, client):
        """Test that localhost is an allowed host."""
        response = client.get("/", headers={"Host": "localhost"})
        assert response.status_code == 200
    
    def test_127_0_0_1_is_allowed(self, client):
        """Test that 127.0.0.1 is an allowed host."""
        response = client.get("/", headers={"Host": "127.0.0.1"})
        assert response.status_code == 200
    
    def test_railway_domain_is_allowed(self, client):
        """Test that Railway domains are allowed."""
        response = client.get("/", headers={"Host": "myapp.railway.app"})
        assert response.status_code == 200
    
    def test_vercel_domain_is_allowed(self, client):
        """Test that Vercel domains are allowed."""
        response = client.get("/", headers={"Host": "myapp.vercel.app"})
        assert response.status_code == 200
    
    def test_invalid_host_is_rejected(self, client):
        """Test that invalid hosts are rejected."""
        response = client.get("/", headers={"Host": "malicious-site.com"})
        # TrustedHostMiddleware returns 400 for invalid hosts
        assert response.status_code == 400
