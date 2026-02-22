"""ChatMessage model for storing chat conversations."""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, Index
from sqlalchemy.sql import func
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class ChatMessage(Base):
    """
    Model for storing chat messages between users and the AI assistant.
    
    Attributes:
        id: Primary key, auto-incrementing integer
        session_id: Groups messages by conversation session (max 100 chars)
        role: Message sender - 'user' or 'assistant' (max 20 chars)
        content: The actual message text
        timestamp: When the message was created (with timezone)
        ip_address: User's IP address for rate limiting (max 45 chars for IPv6)
    """
    
    __tablename__ = "chat_messages"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(String(100), nullable=False, index=True)
    role = Column(String(20), nullable=False)
    content = Column(Text, nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    ip_address = Column(String(45), nullable=True)
    
    __table_args__ = (
        Index('idx_session_timestamp', 'session_id', 'timestamp'),
        Index('idx_timestamp', 'timestamp'),
    )
    
    def __repr__(self) -> str:
        return f"<ChatMessage(id={self.id}, session_id='{self.session_id}', role='{self.role}')>"
