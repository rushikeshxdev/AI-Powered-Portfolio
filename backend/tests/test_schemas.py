"""
Unit tests for Pydantic schemas.

Tests validation rules, sanitization, and error handling for all schema models.
"""

import pytest
from datetime import datetime
from pydantic import ValidationError

from src.schemas import (
    ChatRequest,
    ChatMessage,
    ChatHistoryResponse,
    ErrorResponse,
    DeleteResponse,
    HealthResponse,
    StreamToken,
)


class TestChatRequest:
    """Tests for ChatRequest schema."""
    
    def test_valid_chat_request(self):
        """Test valid chat request with proper question and session_id."""
        request = ChatRequest(
            question="What projects has Rushikesh worked on?",
            session_id="123e4567-e89b-12d3-a456-426614174000"
        )
        assert request.question == "What projects has Rushikesh worked on?"
        assert request.session_id == "123e4567-e89b-12d3-a456-426614174000"
    
    def test_question_too_short(self):
        """Test that empty question is rejected."""
        with pytest.raises(ValidationError) as exc_info:
            ChatRequest(
                question="",
                session_id="123e4567-e89b-12d3-a456-426614174000"
            )
        assert "question" in str(exc_info.value)
    
    def test_question_too_long(self):
        """Test that question exceeding 500 characters is rejected."""
        long_question = "a" * 501
        with pytest.raises(ValidationError) as exc_info:
            ChatRequest(
                question=long_question,
                session_id="123e4567-e89b-12d3-a456-426614174000"
            )
        assert "question" in str(exc_info.value)
    
    def test_question_sanitization_html(self):
        """Test that HTML/XSS characters are removed."""
        request = ChatRequest(
            question="<script>alert('xss')</script>What is your name?",
            session_id="123e4567-e89b-12d3-a456-426614174000"
        )
        assert "<" not in request.question
        assert ">" not in request.question
        assert "script" in request.question  # Text remains
    
    def test_question_sanitization_sql(self):
        """Test that SQL injection characters are removed."""
        request = ChatRequest(
            question="What is your name'; DROP TABLE users; --",
            session_id="123e4567-e89b-12d3-a456-426614174000"
        )
        assert "'" not in request.question
        assert ";" not in request.question
    
    def test_question_sanitization_command_injection(self):
        """Test that command injection characters are removed."""
        request = ChatRequest(
            question="What is `whoami` $USER | cat /etc/passwd",
            session_id="123e4567-e89b-12d3-a456-426614174000"
        )
        assert "`" not in request.question
        assert "$" not in request.question
        assert "|" not in request.question
    
    def test_question_sanitization_ampersand(self):
        """Test that ampersand is replaced with 'and'."""
        request = ChatRequest(
            question="What are React & TypeScript?",
            session_id="123e4567-e89b-12d3-a456-426614174000"
        )
        assert "&" not in request.question
        assert "and" in request.question
    
    def test_question_only_dangerous_chars(self):
        """Test that question with only dangerous chars is rejected."""
        with pytest.raises(ValidationError) as exc_info:
            ChatRequest(
                question="<>;&'\"",
                session_id="123e4567-e89b-12d3-a456-426614174000"
            )
        assert "empty after sanitization" in str(exc_info.value).lower()
    
    def test_valid_uuid_formats(self):
        """Test various valid UUID formats."""
        valid_uuids = [
            "123e4567-e89b-12d3-a456-426614174000",
            "550e8400-e29b-41d4-a716-446655440000",
            "AAAAAAAA-BBBB-CCCC-DDDD-EEEEEEEEEEEE",
        ]
        for uuid in valid_uuids:
            request = ChatRequest(
                question="Test question",
                session_id=uuid
            )
            assert request.session_id == uuid.lower()  # Normalized to lowercase
    
    def test_invalid_session_id_format(self):
        """Test that invalid UUID format is rejected."""
        invalid_uuids = [
            "not-a-uuid",
            "12345678-1234-1234-1234",  # Too short
            "12345678-1234-1234-1234-1234567890123",  # Too long
            "12345678_1234_1234_1234_123456789012",  # Wrong separator
            "",
        ]
        for invalid_uuid in invalid_uuids:
            with pytest.raises(ValidationError) as exc_info:
                ChatRequest(
                    question="Test question",
                    session_id=invalid_uuid
                )
            assert "session_id" in str(exc_info.value).lower()
    
    def test_session_id_normalization(self):
        """Test that session_id is normalized to lowercase."""
        request = ChatRequest(
            question="Test question",
            session_id="AAAAAAAA-BBBB-CCCC-DDDD-EEEEEEEEEEEE"
        )
        assert request.session_id == "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee"


class TestChatMessage:
    """Tests for ChatMessage schema."""
    
    def test_valid_user_message(self):
        """Test valid user message."""
        message = ChatMessage(
            id=1,
            session_id="123e4567-e89b-12d3-a456-426614174000",
            role="user",
            content="What is your name?",
            timestamp=datetime.utcnow()
        )
        assert message.role == "user"
        assert message.content == "What is your name?"
    
    def test_valid_assistant_message(self):
        """Test valid assistant message."""
        message = ChatMessage(
            id=2,
            session_id="123e4567-e89b-12d3-a456-426614174000",
            role="assistant",
            content="I am an AI assistant.",
            timestamp=datetime.utcnow()
        )
        assert message.role == "assistant"
    
    def test_invalid_role(self):
        """Test that invalid role is rejected."""
        with pytest.raises(ValidationError) as exc_info:
            ChatMessage(
                id=1,
                session_id="123e4567-e89b-12d3-a456-426614174000",
                role="admin",  # Invalid role
                content="Test",
                timestamp=datetime.utcnow()
            )
        assert "role" in str(exc_info.value).lower()


class TestChatHistoryResponse:
    """Tests for ChatHistoryResponse schema."""
    
    def test_valid_history_response(self):
        """Test valid chat history response."""
        messages = [
            ChatMessage(
                id=1,
                session_id="123e4567-e89b-12d3-a456-426614174000",
                role="user",
                content="Question 1",
                timestamp=datetime.utcnow()
            ),
            ChatMessage(
                id=2,
                session_id="123e4567-e89b-12d3-a456-426614174000",
                role="assistant",
                content="Answer 1",
                timestamp=datetime.utcnow()
            ),
        ]
        response = ChatHistoryResponse(messages=messages, total=2)
        assert len(response.messages) == 2
        assert response.total == 2
    
    def test_empty_history(self):
        """Test empty chat history."""
        response = ChatHistoryResponse(messages=[], total=0)
        assert len(response.messages) == 0
        assert response.total == 0
    
    def test_total_auto_correction(self):
        """Test that total is auto-corrected to match message count."""
        messages = [
            ChatMessage(
                id=1,
                session_id="123e4567-e89b-12d3-a456-426614174000",
                role="user",
                content="Question",
                timestamp=datetime.utcnow()
            ),
        ]
        # Provide incorrect total
        response = ChatHistoryResponse(messages=messages, total=5)
        # Should be auto-corrected to 1
        assert response.total == 1


class TestErrorResponse:
    """Tests for ErrorResponse schema."""
    
    def test_valid_error_response(self):
        """Test valid error response."""
        error = ErrorResponse(
            error="validation_error",
            detail="Invalid input provided",
            status_code=422
        )
        assert error.error == "validation_error"
        assert error.detail == "Invalid input provided"
        assert error.status_code == 422
    
    def test_error_without_detail(self):
        """Test error response without detail."""
        error = ErrorResponse(
            error="not_found",
            status_code=404
        )
        assert error.detail is None
    
    def test_invalid_status_code(self):
        """Test that invalid status code is rejected."""
        with pytest.raises(ValidationError) as exc_info:
            ErrorResponse(
                error="test_error",
                status_code=200  # Not an error code
            )
        assert "status_code" in str(exc_info.value).lower()
    
    def test_valid_error_status_codes(self):
        """Test various valid error status codes."""
        valid_codes = [400, 401, 403, 404, 422, 429, 500, 502, 503]
        for code in valid_codes:
            error = ErrorResponse(
                error="test_error",
                status_code=code
            )
            assert error.status_code == code


class TestDeleteResponse:
    """Tests for DeleteResponse schema."""
    
    def test_successful_deletion(self):
        """Test successful deletion response."""
        response = DeleteResponse(success=True, deleted_count=5)
        assert response.success is True
        assert response.deleted_count == 5
    
    def test_failed_deletion(self):
        """Test failed deletion response."""
        response = DeleteResponse(success=False, deleted_count=0)
        assert response.success is False
        assert response.deleted_count == 0
    
    def test_negative_deleted_count(self):
        """Test that negative deleted_count is rejected."""
        with pytest.raises(ValidationError) as exc_info:
            DeleteResponse(success=True, deleted_count=-1)
        assert "deleted_count" in str(exc_info.value).lower()


class TestHealthResponse:
    """Tests for HealthResponse schema."""
    
    def test_healthy_status(self):
        """Test healthy status response."""
        response = HealthResponse(
            status="healthy",
            services={"database": True, "vector_store": True}
        )
        assert response.status == "healthy"
        assert response.services["database"] is True
    
    def test_degraded_status(self):
        """Test degraded status response."""
        response = HealthResponse(
            status="degraded",
            services={"database": False, "vector_store": True}
        )
        assert response.status == "degraded"
    
    def test_unhealthy_status(self):
        """Test unhealthy status response."""
        response = HealthResponse(status="unhealthy")
        assert response.status == "unhealthy"
    
    def test_invalid_status(self):
        """Test that invalid status is rejected."""
        with pytest.raises(ValidationError) as exc_info:
            HealthResponse(status="unknown")
        assert "status" in str(exc_info.value).lower()
    
    def test_timestamp_auto_generation(self):
        """Test that timestamp is auto-generated if not provided."""
        response = HealthResponse(status="healthy")
        assert response.timestamp is not None
        assert isinstance(response.timestamp, datetime)


class TestStreamToken:
    """Tests for StreamToken schema."""
    
    def test_token_type(self):
        """Test token type with content."""
        token = StreamToken(type="token", content="Hello")
        assert token.type == "token"
        assert token.content == "Hello"
    
    def test_done_type(self):
        """Test done type without content."""
        token = StreamToken(type="done")
        assert token.type == "done"
        assert token.content is None
    
    def test_invalid_type(self):
        """Test that invalid type is rejected."""
        with pytest.raises(ValidationError) as exc_info:
            StreamToken(type="invalid")
        assert "type" in str(exc_info.value).lower()
