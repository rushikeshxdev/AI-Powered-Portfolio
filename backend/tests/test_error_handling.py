"""
Tests for comprehensive error handling in the FastAPI application.

This module tests:
- Global exception handlers (ValidationError, general Exception)
- Database failure handling (degraded mode)
- OpenRouter API failure handling
- Vector store failure handling
- Appropriate HTTP status codes
"""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, MagicMock, patch
from sqlalchemy.exc import SQLAlchemyError
import httpx

from src.main import app

client = TestClient(app)


@pytest.mark.asyncio
async def test_validation_error_handler():
    """Test global ValidationError handler returns HTTP 422."""
    with TestClient(app) as test_client:
        # Send invalid request (missing required field)
        response = test_client.post(
            "/api/chat",
            json={
                "session_id": "123e4567-e89b-12d3-a456-426614174000"
                # Missing 'question' field
            }
        )
        
        assert response.status_code == 422
        data = response.json()
        assert "error" in data
        assert data["error"] == "validation_error"
        assert "detail" in data


@pytest.mark.asyncio
async def test_database_failure_degraded_mode():
    """Test database failure handling - continue without persistence (degraded mode)."""
    # Mock RAG engine
    mock_rag_engine = MagicMock()
    
    async def mock_process_question(question):
        """Mock RAG engine that yields test tokens."""
        yield "Test"
        yield " response"
    
    mock_rag_engine.process_question = mock_process_question
    
    # Mock database session that raises error
    mock_db_session = AsyncMock()
    mock_chat_repo = AsyncMock()
    mock_chat_repo.save_message.side_effect = SQLAlchemyError("Database connection failed")
    
    with patch("src.main.ChatRepository", return_value=mock_chat_repo):
        with patch("src.main.get_db", return_value=mock_db_session):
            # Set RAG engine in app state
            app.state.rag_engine = mock_rag_engine
            
            with TestClient(app) as test_client:
                response = test_client.post(
                    "/api/chat",
                    json={
                        "question": "Test question",
                        "session_id": "123e4567-e89b-12d3-a456-426614174000"
                    }
                )
                
                # Should still return 200 (degraded mode)
                assert response.status_code == 200
                
                # Should contain response tokens
                content = response.text
                assert "data:" in content
                
                # Verify rollback was called
                assert mock_db_session.rollback.called


@pytest.mark.asyncio
async def test_openrouter_api_failure_handling():
    """Test OpenRouter API failure returns user-friendly error message."""
    # Mock RAG engine that raises HTTPError
    mock_rag_engine = MagicMock()
    
    async def mock_process_question(question):
        """Mock RAG engine that raises HTTPError."""
        raise httpx.HTTPError("OpenRouter API unavailable")
    
    mock_rag_engine.process_question = mock_process_question
    
    # Mock database session
    mock_db_session = AsyncMock()
    mock_chat_repo = AsyncMock()
    
    with patch("src.main.ChatRepository", return_value=mock_chat_repo):
        with patch("src.main.get_db", return_value=mock_db_session):
            # Set RAG engine in app state
            app.state.rag_engine = mock_rag_engine
            
            with TestClient(app) as test_client:
                response = test_client.post(
                    "/api/chat",
                    json={
                        "question": "Test question",
                        "session_id": "123e4567-e89b-12d3-a456-426614174000"
                    }
                )
                
                # Should return 200 (SSE stream)
                assert response.status_code == 200
                
                # Should contain error message in SSE format
                content = response.text
                assert "data:" in content
                assert "error" in content
                assert "AI service temporarily unavailable" in content


@pytest.mark.asyncio
async def test_vector_store_failure_fallback():
    """Test vector store failure returns appropriate error message."""
    # Mock RAG engine that raises vector store error
    mock_rag_engine = MagicMock()
    
    async def mock_process_question(question):
        """Mock RAG engine that raises vector store error."""
        raise Exception("ChromaDB connection failed")
    
    mock_rag_engine.process_question = mock_process_question
    
    # Mock database session
    mock_db_session = AsyncMock()
    mock_chat_repo = AsyncMock()
    
    with patch("src.main.ChatRepository", return_value=mock_chat_repo):
        with patch("src.main.get_db", return_value=mock_db_session):
            # Set RAG engine in app state
            app.state.rag_engine = mock_rag_engine
            
            with TestClient(app) as test_client:
                response = test_client.post(
                    "/api/chat",
                    json={
                        "question": "Test question",
                        "session_id": "123e4567-e89b-12d3-a456-426614174000"
                    }
                )
                
                # Should return 200 (SSE stream)
                assert response.status_code == 200
                
                # Should contain error message in SSE format
                content = response.text
                assert "data:" in content
                assert "error" in content
                assert "Unable to retrieve context" in content or "error occurred" in content


@pytest.mark.asyncio
async def test_rag_engine_not_initialized_returns_503():
    """Test chat endpoint returns 503 if RAG engine is not initialized."""
    with TestClient(app) as test_client:
        # Remove RAG engine from app state if it exists
        if hasattr(app.state, "rag_engine"):
            delattr(app.state, "rag_engine")
        
        response = test_client.post(
            "/api/chat",
            json={
                "question": "Test question",
                "session_id": "123e4567-e89b-12d3-a456-426614174000"
            }
        )
        
        assert response.status_code == 503
        data = response.json()
        assert "AI service is not available" in data["detail"]


@pytest.mark.asyncio
async def test_rate_limit_returns_429():
    """Test rate limit exceeded returns HTTP 429 with Retry-After header."""
    # Mock RAG engine
    mock_rag_engine = MagicMock()
    
    async def mock_process_question(question):
        """Mock RAG engine that yields test tokens."""
        yield "Test"
    
    mock_rag_engine.process_question = mock_process_question
    
    # Mock database session
    mock_db_session = AsyncMock()
    mock_chat_repo = AsyncMock()
    
    with patch("src.main.ChatRepository", return_value=mock_chat_repo):
        with patch("src.main.get_db", return_value=mock_db_session):
            # Set RAG engine in app state
            app.state.rag_engine = mock_rag_engine
            
            with TestClient(app) as test_client:
                # Make 10 requests (should all succeed)
                for i in range(10):
                    response = test_client.post(
                        "/api/chat",
                        json={
                            "question": f"Test question {i}",
                            "session_id": "123e4567-e89b-12d3-a456-426614174000"
                        }
                    )
                    assert response.status_code == 200
                
                # 11th request should be rate limited
                response = test_client.post(
                    "/api/chat",
                    json={
                        "question": "Test question 11",
                        "session_id": "123e4567-e89b-12d3-a456-426614174000"
                    }
                )
                
                # Should return 429
                assert response.status_code == 429
                
                # Check error response format
                data = response.json()
                assert "error" in data
                assert data["error"] == "rate_limit_exceeded"
                
                # Check Retry-After header
                assert "retry-after" in response.headers
                assert response.headers["retry-after"] == "60"


@pytest.mark.asyncio
async def test_invalid_request_returns_422():
    """Test invalid request payload returns HTTP 422."""
    with TestClient(app) as test_client:
        # Test with invalid session_id format
        response = test_client.post(
            "/api/chat",
            json={
                "question": "Test question",
                "session_id": "invalid-uuid"
            }
        )
        
        assert response.status_code == 422
        data = response.json()
        assert "error" in data


@pytest.mark.asyncio
async def test_database_error_on_assistant_message_storage():
    """Test database error when storing assistant message doesn't fail request."""
    # Mock RAG engine
    mock_rag_engine = MagicMock()
    
    async def mock_process_question(question):
        """Mock RAG engine that yields test tokens."""
        yield "Test"
        yield " response"
    
    mock_rag_engine.process_question = mock_process_question
    
    # Mock database session
    mock_db_session = AsyncMock()
    mock_chat_repo = AsyncMock()
    
    # First call (user message) succeeds, second call (assistant message) fails
    call_count = 0
    async def save_message_side_effect(*args, **kwargs):
        nonlocal call_count
        call_count += 1
        if call_count == 2:  # Second call (assistant message)
            raise SQLAlchemyError("Database error")
        return MagicMock()
    
    mock_chat_repo.save_message.side_effect = save_message_side_effect
    
    with patch("src.main.ChatRepository", return_value=mock_chat_repo):
        with patch("src.main.get_db", return_value=mock_db_session):
            # Set RAG engine in app state
            app.state.rag_engine = mock_rag_engine
            
            with TestClient(app) as test_client:
                response = test_client.post(
                    "/api/chat",
                    json={
                        "question": "Test question",
                        "session_id": "123e4567-e89b-12d3-a456-426614174000"
                    }
                )
                
                # Should still return 200 (user got the response)
                assert response.status_code == 200
                
                # Should contain response tokens
                content = response.text
                assert "data:" in content
                assert "Test" in content or "response" in content


@pytest.mark.asyncio
async def test_unexpected_error_in_sse_stream():
    """Test unexpected error in SSE stream generation returns error message."""
    # Mock RAG engine that raises unexpected error
    mock_rag_engine = MagicMock()
    
    async def mock_process_question(question):
        """Mock RAG engine that raises unexpected error."""
        raise RuntimeError("Unexpected error")
    
    mock_rag_engine.process_question = mock_process_question
    
    # Mock database session
    mock_db_session = AsyncMock()
    mock_chat_repo = AsyncMock()
    
    with patch("src.main.ChatRepository", return_value=mock_chat_repo):
        with patch("src.main.get_db", return_value=mock_db_session):
            # Set RAG engine in app state
            app.state.rag_engine = mock_rag_engine
            
            with TestClient(app) as test_client:
                response = test_client.post(
                    "/api/chat",
                    json={
                        "question": "Test question",
                        "session_id": "123e4567-e89b-12d3-a456-426614174000"
                    }
                )
                
                # Should return 200 (SSE stream)
                assert response.status_code == 200
                
                # Should contain error message
                content = response.text
                assert "data:" in content
                assert "error" in content


@pytest.mark.asyncio
async def test_http_status_codes_correctness():
    """Test that appropriate HTTP status codes are returned for different error conditions."""
    with TestClient(app) as test_client:
        # 422 for validation errors
        response = test_client.post(
            "/api/chat",
            json={"session_id": "invalid"}
        )
        assert response.status_code == 422
        
        # 503 for service unavailable (RAG engine not initialized)
        if hasattr(app.state, "rag_engine"):
            delattr(app.state, "rag_engine")
        
        response = test_client.post(
            "/api/chat",
            json={
                "question": "Test",
                "session_id": "123e4567-e89b-12d3-a456-426614174000"
            }
        )
        assert response.status_code == 503
