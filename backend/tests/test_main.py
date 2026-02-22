"""
Tests for main FastAPI application.
"""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, MagicMock, patch
from src.main import app

client = TestClient(app)


def test_root_endpoint():
    """Test root endpoint returns API information."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "AI Portfolio Backend API"
    assert data["version"] == "1.0.0"
    assert "docs" in data


def test_health_check_all_services_healthy():
    """Test health check endpoint returns healthy status when all services are operational."""
    from unittest.mock import MagicMock, AsyncMock, patch
    from sqlalchemy import text
    
    # Mock database session
    mock_db_session = AsyncMock()
    mock_result = MagicMock()
    mock_result.fetchone.return_value = (1,)
    mock_db_session.execute.return_value = mock_result
    
    # Mock vector store
    mock_vector_store = MagicMock()
    mock_vector_store.get_collection_count.return_value = 10
    
    with patch("src.main.get_db", return_value=mock_db_session):
        # Set vector store in app state
        app.state.vector_store = mock_vector_store
        
        with TestClient(app) as test_client:
            response = test_client.get("/api/health")
            
            assert response.status_code == 200
            data = response.json()
            assert data["status"] == "healthy"
            assert data["services"]["database"] is True
            assert data["services"]["vector_store"] is True
            assert "timestamp" in data


def test_health_check_database_unavailable():
    """Test health check endpoint returns degraded status when database is unavailable."""
    from unittest.mock import MagicMock, AsyncMock, patch
    
    # Mock database session that raises exception
    mock_db_session = AsyncMock()
    mock_db_session.execute.side_effect = Exception("Database connection failed")
    
    # Mock vector store (healthy)
    mock_vector_store = MagicMock()
    mock_vector_store.get_collection_count.return_value = 10
    
    with patch("src.main.get_db", return_value=mock_db_session):
        # Set vector store in app state
        app.state.vector_store = mock_vector_store
        
        with TestClient(app) as test_client:
            response = test_client.get("/api/health")
            
            assert response.status_code == 503
            data = response.json()
            assert data["status"] == "degraded"
            assert data["services"]["database"] is False
            assert data["services"]["vector_store"] is True


def test_health_check_vector_store_unavailable():
    """Test health check endpoint returns degraded status when vector store is unavailable."""
    from unittest.mock import MagicMock, AsyncMock, patch
    from sqlalchemy import text
    
    # Mock database session (healthy)
    mock_db_session = AsyncMock()
    mock_result = MagicMock()
    mock_result.fetchone.return_value = (1,)
    mock_db_session.execute.return_value = mock_result
    
    # Mock vector store that raises exception
    mock_vector_store = MagicMock()
    mock_vector_store.get_collection_count.side_effect = Exception("Vector store connection failed")
    
    with patch("src.main.get_db", return_value=mock_db_session):
        # Set vector store in app state
        app.state.vector_store = mock_vector_store
        
        with TestClient(app) as test_client:
            response = test_client.get("/api/health")
            
            assert response.status_code == 503
            data = response.json()
            assert data["status"] == "degraded"
            assert data["services"]["database"] is True
            assert data["services"]["vector_store"] is False


def test_health_check_all_services_unavailable():
    """Test health check endpoint returns degraded status when all services are unavailable."""
    from unittest.mock import MagicMock, AsyncMock, patch
    
    # Mock database session that raises exception
    mock_db_session = AsyncMock()
    mock_db_session.execute.side_effect = Exception("Database connection failed")
    
    # Mock vector store that raises exception
    mock_vector_store = MagicMock()
    mock_vector_store.get_collection_count.side_effect = Exception("Vector store connection failed")
    
    with patch("src.main.get_db", return_value=mock_db_session):
        # Set vector store in app state
        app.state.vector_store = mock_vector_store
        
        with TestClient(app) as test_client:
            response = test_client.get("/api/health")
            
            assert response.status_code == 503
            data = response.json()
            assert data["status"] == "degraded"
            assert data["services"]["database"] is False
            assert data["services"]["vector_store"] is False


def test_cors_headers():
    """Test CORS headers are present in responses."""
    response = client.get("/health", headers={"Origin": "http://localhost:5173"})
    assert response.status_code == 200
    # CORS headers should be present
    assert "access-control-allow-origin" in response.headers


@pytest.mark.asyncio
async def test_chat_endpoint_requires_rag_engine():
    """Test chat endpoint returns 503 if RAG engine is not initialized."""
    # Create a test client without RAG engine initialized
    with TestClient(app) as test_client:
        # Remove RAG engine from app state if it exists
        if hasattr(app.state, "rag_engine"):
            delattr(app.state, "rag_engine")
        
        response = test_client.post(
            "/api/chat",
            json={
                "question": "What projects has Rushikesh worked on?",
                "session_id": "123e4567-e89b-12d3-a456-426614174000"
            }
        )
        
        assert response.status_code == 503
        assert "AI service is not available" in response.json()["detail"]


@pytest.mark.asyncio
async def test_chat_endpoint_validates_request():
    """Test chat endpoint validates request payload."""
    with TestClient(app) as test_client:
        # Test with missing question
        response = test_client.post(
            "/api/chat",
            json={
                "session_id": "123e4567-e89b-12d3-a456-426614174000"
            }
        )
        assert response.status_code == 422
        
        # Test with invalid session_id format
        response = test_client.post(
            "/api/chat",
            json={
                "question": "Test question",
                "session_id": "invalid-uuid"
            }
        )
        assert response.status_code == 422
        
        # Test with empty question
        response = test_client.post(
            "/api/chat",
            json={
                "question": "",
                "session_id": "123e4567-e89b-12d3-a456-426614174000"
            }
        )
        assert response.status_code == 422


@pytest.mark.asyncio
async def test_chat_endpoint_returns_sse_stream():
    """Test chat endpoint returns Server-Sent Events stream."""
    # Mock the RAG engine and database
    mock_rag_engine = MagicMock()
    
    async def mock_process_question(question):
        """Mock RAG engine that yields test tokens."""
        yield "Hello"
        yield " "
        yield "world"
    
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
                        "question": "What projects has Rushikesh worked on?",
                        "session_id": "123e4567-e89b-12d3-a456-426614174000"
                    }
                )
                
                # Check response headers
                assert response.status_code == 200
                assert response.headers["content-type"] == "text/event-stream; charset=utf-8"
                assert response.headers["cache-control"] == "no-cache"
                
                # Check response contains SSE formatted data
                content = response.text
                assert "data:" in content
                assert '"type":"token"' in content or '"type": "token"' in content



@pytest.mark.asyncio
async def test_rate_limiting():
    """Test rate limiting on chat endpoint (10 requests per minute per IP)."""
    import time
    
    # Mock the RAG engine and database
    mock_rag_engine = MagicMock()
    
    async def mock_process_question(question):
        """Mock RAG engine that yields test tokens."""
        yield "Test"
        yield " response"
    
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
                    assert response.status_code == 200, f"Request {i+1} failed"
                
                # 11th request should be rate limited
                response = test_client.post(
                    "/api/chat",
                    json={
                        "question": "Test question 11",
                        "session_id": "123e4567-e89b-12d3-a456-426614174000"
                    }
                )
                
                # Should return 429 Too Many Requests
                assert response.status_code == 429
                
                # Check response contains error message
                data = response.json()
                assert "error" in data
                assert "Rate limit exceeded" in data["error"]
                
                # Check Retry-After header is present
                assert "retry-after" in response.headers
                assert response.headers["retry-after"] == "60"


def test_get_client_ip_with_forwarded_header():
    """Test IP extraction from X-Forwarded-For header."""
    from src.main import get_client_ip_for_limiter
    from fastapi import Request
    
    # Mock request with X-Forwarded-For header
    mock_request = MagicMock(spec=Request)
    mock_request.headers.get.return_value = "192.168.1.1, 10.0.0.1"
    
    ip = get_client_ip_for_limiter(mock_request)
    assert ip == "192.168.1.1"


def test_get_client_ip_without_forwarded_header():
    """Test IP extraction from client.host when no X-Forwarded-For header."""
    from src.main import get_client_ip_for_limiter
    from fastapi import Request
    
    # Mock request without X-Forwarded-For header
    mock_request = MagicMock(spec=Request)
    mock_request.headers.get.return_value = None
    mock_request.client.host = "192.168.1.100"
    
    ip = get_client_ip_for_limiter(mock_request)
    assert ip == "192.168.1.100"


def test_get_client_ip_no_client():
    """Test IP extraction when client is None."""
    from src.main import get_client_ip_for_limiter
    from fastapi import Request
    
    # Mock request with no client
    mock_request = MagicMock(spec=Request)
    mock_request.headers.get.return_value = None
    mock_request.client = None
    
    ip = get_client_ip_for_limiter(mock_request)
    assert ip == "unknown"



@pytest.mark.asyncio
async def test_get_chat_history_success():
    """Test GET /api/chat/history/{session_id} returns messages."""
    from datetime import datetime
    from src.models.chat_message import ChatMessage as ChatMessageModel
    
    # Mock database session and repository
    mock_db_session = AsyncMock()
    
    # Create mock messages
    mock_messages = [
        ChatMessageModel(
            id=1,
            session_id="123e4567-e89b-12d3-a456-426614174000",
            role="user",
            content="Test question",
            timestamp=datetime(2024, 1, 1, 10, 0, 0),
            ip_address="192.168.1.1"
        ),
        ChatMessageModel(
            id=2,
            session_id="123e4567-e89b-12d3-a456-426614174000",
            role="assistant",
            content="Test answer",
            timestamp=datetime(2024, 1, 1, 10, 0, 5),
            ip_address="192.168.1.1"
        )
    ]
    
    mock_chat_repo = AsyncMock()
    mock_chat_repo.get_history.return_value = mock_messages
    
    with patch("src.main.ChatRepository", return_value=mock_chat_repo):
        with patch("src.main.get_db", return_value=mock_db_session):
            with TestClient(app) as test_client:
                response = test_client.get(
                    "/api/chat/history/123e4567-e89b-12d3-a456-426614174000"
                )
                
                assert response.status_code == 200
                data = response.json()
                
                # Check response structure
                assert "messages" in data
                assert "total" in data
                assert data["total"] == 2
                assert len(data["messages"]) == 2
                
                # Check first message
                assert data["messages"][0]["role"] == "user"
                assert data["messages"][0]["content"] == "Test question"
                
                # Check second message
                assert data["messages"][1]["role"] == "assistant"
                assert data["messages"][1]["content"] == "Test answer"


@pytest.mark.asyncio
async def test_get_chat_history_with_limit():
    """Test GET /api/chat/history/{session_id} respects limit parameter."""
    from datetime import datetime
    from src.models.chat_message import ChatMessage as ChatMessageModel
    
    # Mock database session and repository
    mock_db_session = AsyncMock()
    
    # Create mock messages (only 2 returned due to limit)
    mock_messages = [
        ChatMessageModel(
            id=1,
            session_id="123e4567-e89b-12d3-a456-426614174000",
            role="user",
            content="Question 1",
            timestamp=datetime(2024, 1, 1, 10, 0, 0),
            ip_address="192.168.1.1"
        ),
        ChatMessageModel(
            id=2,
            session_id="123e4567-e89b-12d3-a456-426614174000",
            role="assistant",
            content="Answer 1",
            timestamp=datetime(2024, 1, 1, 10, 0, 5),
            ip_address="192.168.1.1"
        )
    ]
    
    mock_chat_repo = AsyncMock()
    mock_chat_repo.get_history.return_value = mock_messages
    
    with patch("src.main.ChatRepository", return_value=mock_chat_repo):
        with patch("src.main.get_db", return_value=mock_db_session):
            with TestClient(app) as test_client:
                response = test_client.get(
                    "/api/chat/history/123e4567-e89b-12d3-a456-426614174000?limit=2"
                )
                
                assert response.status_code == 200
                data = response.json()
                assert data["total"] == 2
                
                # Verify repository was called with correct limit
                mock_chat_repo.get_history.assert_called_once()
                call_args = mock_chat_repo.get_history.call_args
                assert call_args.kwargs["limit"] == 2


@pytest.mark.asyncio
async def test_get_chat_history_empty():
    """Test GET /api/chat/history/{session_id} returns empty list for new session."""
    # Mock database session and repository
    mock_db_session = AsyncMock()
    
    mock_chat_repo = AsyncMock()
    mock_chat_repo.get_history.return_value = []
    
    with patch("src.main.ChatRepository", return_value=mock_chat_repo):
        with patch("src.main.get_db", return_value=mock_db_session):
            with TestClient(app) as test_client:
                response = test_client.get(
                    "/api/chat/history/123e4567-e89b-12d3-a456-426614174000"
                )
                
                assert response.status_code == 200
                data = response.json()
                assert data["messages"] == []
                assert data["total"] == 0


@pytest.mark.asyncio
async def test_get_chat_history_invalid_uuid():
    """Test GET /api/chat/history/{session_id} returns 422 for invalid UUID."""
    with TestClient(app) as test_client:
        response = test_client.get("/api/chat/history/invalid-uuid")
        
        assert response.status_code == 422
        data = response.json()
        assert "session_id must be a valid UUID format" in data["detail"]


@pytest.mark.asyncio
async def test_get_chat_history_limit_constraints():
    """Test GET /api/chat/history/{session_id} enforces limit constraints."""
    from datetime import datetime
    from src.models.chat_message import ChatMessage as ChatMessageModel
    
    # Mock database session and repository
    mock_db_session = AsyncMock()
    mock_messages = []
    
    mock_chat_repo = AsyncMock()
    mock_chat_repo.get_history.return_value = mock_messages
    
    with patch("src.main.ChatRepository", return_value=mock_chat_repo):
        with patch("src.main.get_db", return_value=mock_db_session):
            with TestClient(app) as test_client:
                # Test limit below minimum (should fail validation)
                response = test_client.get(
                    "/api/chat/history/123e4567-e89b-12d3-a456-426614174000?limit=0"
                )
                assert response.status_code == 422
                
                # Test limit above maximum (should fail validation)
                response = test_client.get(
                    "/api/chat/history/123e4567-e89b-12d3-a456-426614174000?limit=101"
                )
                assert response.status_code == 422
                
                # Test valid limit at boundary (1)
                response = test_client.get(
                    "/api/chat/history/123e4567-e89b-12d3-a456-426614174000?limit=1"
                )
                assert response.status_code == 200
                
                # Test valid limit at boundary (100)
                response = test_client.get(
                    "/api/chat/history/123e4567-e89b-12d3-a456-426614174000?limit=100"
                )
                assert response.status_code == 200


@pytest.mark.asyncio
async def test_get_chat_history_default_limit():
    """Test GET /api/chat/history/{session_id} uses default limit of 50."""
    # Mock database session and repository
    mock_db_session = AsyncMock()
    
    mock_chat_repo = AsyncMock()
    mock_chat_repo.get_history.return_value = []
    
    with patch("src.main.ChatRepository", return_value=mock_chat_repo):
        with patch("src.main.get_db", return_value=mock_db_session):
            with TestClient(app) as test_client:
                response = test_client.get(
                    "/api/chat/history/123e4567-e89b-12d3-a456-426614174000"
                )
                
                assert response.status_code == 200
                
                # Verify repository was called with default limit of 50
                mock_chat_repo.get_history.assert_called_once()
                call_args = mock_chat_repo.get_history.call_args
                assert call_args.kwargs["limit"] == 50



@pytest.mark.asyncio
async def test_delete_chat_history_success():
    """Test DELETE /api/chat/history/{session_id} deletes messages successfully."""
    # Mock database session and repository
    mock_db_session = AsyncMock()
    
    mock_chat_repo = AsyncMock()
    mock_chat_repo.delete_session.return_value = 5  # 5 messages deleted
    
    with patch("src.main.ChatRepository", return_value=mock_chat_repo):
        with patch("src.main.get_db", return_value=mock_db_session):
            with TestClient(app) as test_client:
                response = test_client.delete(
                    "/api/chat/history/123e4567-e89b-12d3-a456-426614174000"
                )
                
                assert response.status_code == 200
                data = response.json()
                
                # Check response structure
                assert "success" in data
                assert "deleted_count" in data
                assert data["success"] is True
                assert data["deleted_count"] == 5
                
                # Verify repository was called
                mock_chat_repo.delete_session.assert_called_once_with(
                    "123e4567-e89b-12d3-a456-426614174000"
                )
                
                # Verify commit was called
                mock_db_session.commit.assert_called_once()


@pytest.mark.asyncio
async def test_delete_chat_history_empty_session():
    """Test DELETE /api/chat/history/{session_id} returns success for empty session (idempotent)."""
    # Mock database session and repository
    mock_db_session = AsyncMock()
    
    mock_chat_repo = AsyncMock()
    mock_chat_repo.delete_session.return_value = 0  # No messages to delete
    
    with patch("src.main.ChatRepository", return_value=mock_chat_repo):
        with patch("src.main.get_db", return_value=mock_db_session):
            with TestClient(app) as test_client:
                response = test_client.delete(
                    "/api/chat/history/123e4567-e89b-12d3-a456-426614174000"
                )
                
                assert response.status_code == 200
                data = response.json()
                
                # Should return success even with 0 deleted (idempotent)
                assert data["success"] is True
                assert data["deleted_count"] == 0


@pytest.mark.asyncio
async def test_delete_chat_history_invalid_uuid():
    """Test DELETE /api/chat/history/{session_id} returns 422 for invalid UUID."""
    with TestClient(app) as test_client:
        response = test_client.delete("/api/chat/history/invalid-uuid")
        
        assert response.status_code == 422
        data = response.json()
        assert "session_id must be a valid UUID format" in data["detail"]


@pytest.mark.asyncio
async def test_delete_chat_history_database_error():
    """Test DELETE /api/chat/history/{session_id} returns 500 on database error."""
    # Mock database session and repository
    mock_db_session = AsyncMock()
    
    mock_chat_repo = AsyncMock()
    mock_chat_repo.delete_session.side_effect = Exception("Database error")
    
    with patch("src.main.ChatRepository", return_value=mock_chat_repo):
        with patch("src.main.get_db", return_value=mock_db_session):
            with TestClient(app) as test_client:
                response = test_client.delete(
                    "/api/chat/history/123e4567-e89b-12d3-a456-426614174000"
                )
                
                assert response.status_code == 500
                data = response.json()
                assert "Failed to delete chat history" in data["detail"]
                
                # Verify rollback was called
                mock_db_session.rollback.assert_called_once()


@pytest.mark.asyncio
async def test_delete_chat_history_normalizes_uuid():
    """Test DELETE /api/chat/history/{session_id} normalizes UUID to lowercase."""
    # Mock database session and repository
    mock_db_session = AsyncMock()
    
    mock_chat_repo = AsyncMock()
    mock_chat_repo.delete_session.return_value = 3
    
    with patch("src.main.ChatRepository", return_value=mock_chat_repo):
        with patch("src.main.get_db", return_value=mock_db_session):
            with TestClient(app) as test_client:
                # Send uppercase UUID
                response = test_client.delete(
                    "/api/chat/history/123E4567-E89B-12D3-A456-426614174000"
                )
                
                assert response.status_code == 200
                
                # Verify repository was called with lowercase UUID
                mock_chat_repo.delete_session.assert_called_once_with(
                    "123e4567-e89b-12d3-a456-426614174000"
                )
