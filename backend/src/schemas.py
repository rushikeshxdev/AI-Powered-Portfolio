"""
Pydantic schemas for request/response validation.

This module defines all Pydantic models used for API request validation
and response serialization, including input sanitization and validation rules.
"""

from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field, field_validator, UUID4
import re


class ChatRequest(BaseModel):
    """
    Request schema for chat endpoint.
    
    Validates user questions with length constraints and input sanitization.
    Validates session_id as UUID format.
    """
    question: str = Field(
        ...,
        min_length=1,
        max_length=500,
        description="User question (1-500 characters)"
    )
    session_id: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Session identifier (UUID format)"
    )
    
    @field_validator('question')
    @classmethod
    def sanitize_question(cls, v: str) -> str:
        """
        Sanitize user input to remove dangerous characters.
        
        Removes or escapes characters that could be used for:
        - XSS attacks: <, >, &
        - SQL injection: single quotes, double quotes
        - Command injection: backticks, semicolons
        
        Args:
            v: Raw question string
            
        Returns:
            Sanitized question string
            
        Raises:
            ValueError: If question contains only whitespace after sanitization
        """
        # Remove dangerous HTML/script characters
        v = v.replace('<', '').replace('>', '').replace('&', 'and')
        
        # Remove potential SQL injection characters
        v = v.replace("'", "").replace('"', '').replace(';', '')
        
        # Remove command injection characters
        v = v.replace('`', '').replace('$', '').replace('|', '')
        
        # Remove null bytes
        v = v.replace('\x00', '')
        
        # Strip leading/trailing whitespace
        v = v.strip()
        
        # Validate not empty after sanitization
        if not v:
            raise ValueError("Question cannot be empty after sanitization")
        
        return v
    
    @field_validator('session_id')
    @classmethod
    def validate_session_id(cls, v: str) -> str:
        """
        Validate session_id is in UUID format.
        
        Args:
            v: Session ID string
            
        Returns:
            Validated session ID
            
        Raises:
            ValueError: If session_id is not a valid UUID format
        """
        # UUID format: 8-4-4-4-12 hexadecimal characters
        uuid_pattern = re.compile(
            r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$',
            re.IGNORECASE
        )
        
        if not uuid_pattern.match(v):
            raise ValueError(
                "session_id must be a valid UUID format "
                "(e.g., '123e4567-e89b-12d3-a456-426614174000')"
            )
        
        return v.lower()  # Normalize to lowercase


class ChatMessage(BaseModel):
    """
    Schema for a single chat message.
    
    Used in chat history responses and message display.
    """
    id: int = Field(..., description="Message ID")
    session_id: str = Field(..., description="Session identifier")
    role: str = Field(..., description="Message role: 'user' or 'assistant'")
    content: str = Field(..., description="Message content")
    timestamp: datetime = Field(..., description="Message timestamp")
    
    @field_validator('role')
    @classmethod
    def validate_role(cls, v: str) -> str:
        """
        Validate role is either 'user' or 'assistant'.
        
        Args:
            v: Role string
            
        Returns:
            Validated role
            
        Raises:
            ValueError: If role is not 'user' or 'assistant'
        """
        if v not in ['user', 'assistant']:
            raise ValueError("role must be 'user' or 'assistant'")
        return v
    
    class Config:
        """Pydantic configuration."""
        from_attributes = True  # Allow ORM model conversion


class ChatHistoryResponse(BaseModel):
    """
    Response schema for chat history endpoint.
    
    Returns list of messages and total count.
    """
    messages: List[ChatMessage] = Field(
        default_factory=list,
        description="List of chat messages"
    )
    total: int = Field(..., description="Total number of messages")
    
    @field_validator('total')
    @classmethod
    def validate_total(cls, v: int, info) -> int:
        """
        Validate total matches message count.
        
        Args:
            v: Total count
            info: Validation info containing other fields
            
        Returns:
            Validated total
        """
        # Note: info.data contains already-validated fields
        messages = info.data.get('messages', [])
        if v != len(messages):
            # Auto-correct to match actual message count
            return len(messages)
        return v


class ErrorResponse(BaseModel):
    """
    Standard error response schema.
    
    Used for all error responses with consistent structure.
    """
    error: str = Field(..., description="Error type/code")
    detail: Optional[str] = Field(
        None,
        description="Detailed error message"
    )
    status_code: int = Field(..., description="HTTP status code")
    
    @field_validator('status_code')
    @classmethod
    def validate_status_code(cls, v: int) -> int:
        """
        Validate status_code is a valid HTTP error code.
        
        Args:
            v: Status code
            
        Returns:
            Validated status code
            
        Raises:
            ValueError: If status code is not in valid error range
        """
        if not (400 <= v < 600):
            raise ValueError("status_code must be a valid HTTP error code (400-599)")
        return v


class DeleteResponse(BaseModel):
    """
    Response schema for delete operations.
    
    Used when deleting chat history.
    """
    success: bool = Field(..., description="Whether deletion was successful")
    deleted_count: int = Field(..., description="Number of messages deleted")
    
    @field_validator('deleted_count')
    @classmethod
    def validate_deleted_count(cls, v: int) -> int:
        """
        Validate deleted_count is non-negative.
        
        Args:
            v: Deleted count
            
        Returns:
            Validated count
            
        Raises:
            ValueError: If count is negative
        """
        if v < 0:
            raise ValueError("deleted_count cannot be negative")
        return v


class HealthResponse(BaseModel):
    """
    Response schema for health check endpoint.
    
    Indicates service health status.
    """
    status: str = Field(..., description="Health status: 'healthy' or 'degraded'")
    timestamp: datetime = Field(
        default_factory=datetime.utcnow,
        description="Health check timestamp"
    )
    services: Optional[dict] = Field(
        None,
        description="Status of individual services (database, vector_store, etc.)"
    )
    
    @field_validator('status')
    @classmethod
    def validate_status(cls, v: str) -> str:
        """
        Validate status is a known health state.
        
        Args:
            v: Status string
            
        Returns:
            Validated status
            
        Raises:
            ValueError: If status is not recognized
        """
        valid_statuses = ['healthy', 'degraded', 'unhealthy']
        if v not in valid_statuses:
            raise ValueError(f"status must be one of {valid_statuses}")
        return v


class StreamToken(BaseModel):
    """
    Schema for streaming response tokens.
    
    Used in Server-Sent Events (SSE) streaming.
    """
    type: str = Field(..., description="Token type: 'token' or 'done'")
    content: Optional[str] = Field(None, description="Token content (if type='token')")
    
    @field_validator('type')
    @classmethod
    def validate_type(cls, v: str) -> str:
        """
        Validate type is either 'token' or 'done'.
        
        Args:
            v: Type string
            
        Returns:
            Validated type
            
        Raises:
            ValueError: If type is not recognized
        """
        if v not in ['token', 'done']:
            raise ValueError("type must be 'token' or 'done'")
        return v
