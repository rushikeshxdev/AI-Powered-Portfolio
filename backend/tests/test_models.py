"""Tests for database models."""

import pytest
from datetime import datetime
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy import select

from src.models.chat_message import ChatMessage, Base


@pytest.fixture
async def db_session():
    """Create an in-memory SQLite database for testing."""
    # Create async engine with in-memory SQLite
    engine = create_async_engine(
        "sqlite+aiosqlite:///:memory:",
        echo=False,
    )
    
    # Create tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    # Create session factory
    async_session = async_sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )
    
    # Provide session
    async with async_session() as session:
        yield session
    
    # Cleanup
    await engine.dispose()


@pytest.mark.asyncio
async def test_chat_message_creation(db_session):
    """Test creating a ChatMessage instance."""
    # Create a message
    message = ChatMessage(
        session_id="test_session_123",
        role="user",
        content="What projects has Rushikesh worked on?",
        ip_address="192.168.1.1"
    )
    
    db_session.add(message)
    await db_session.commit()
    await db_session.refresh(message)
    
    # Verify the message was created
    assert message.id is not None
    assert message.session_id == "test_session_123"
    assert message.role == "user"
    assert message.content == "What projects has Rushikesh worked on?"
    assert message.ip_address == "192.168.1.1"
    assert message.timestamp is not None
    assert isinstance(message.timestamp, datetime)


@pytest.mark.asyncio
async def test_chat_message_query_by_session(db_session):
    """Test querying messages by session_id."""
    # Create multiple messages
    messages = [
        ChatMessage(
            session_id="session_1",
            role="user",
            content="Question 1",
            ip_address="192.168.1.1"
        ),
        ChatMessage(
            session_id="session_1",
            role="assistant",
            content="Answer 1",
            ip_address="192.168.1.1"
        ),
        ChatMessage(
            session_id="session_2",
            role="user",
            content="Question 2",
            ip_address="192.168.1.2"
        ),
    ]
    
    for msg in messages:
        db_session.add(msg)
    await db_session.commit()
    
    # Query messages for session_1
    result = await db_session.execute(
        select(ChatMessage)
        .where(ChatMessage.session_id == "session_1")
        .order_by(ChatMessage.timestamp)
    )
    session_1_messages = result.scalars().all()
    
    # Verify results
    assert len(session_1_messages) == 2
    assert session_1_messages[0].role == "user"
    assert session_1_messages[1].role == "assistant"


@pytest.mark.asyncio
async def test_chat_message_without_ip_address(db_session):
    """Test creating a message without IP address (nullable field)."""
    message = ChatMessage(
        session_id="test_session",
        role="assistant",
        content="This is a response",
        ip_address=None
    )
    
    db_session.add(message)
    await db_session.commit()
    await db_session.refresh(message)
    
    assert message.id is not None
    assert message.ip_address is None


@pytest.mark.asyncio
async def test_chat_message_repr(db_session):
    """Test the string representation of ChatMessage."""
    message = ChatMessage(
        session_id="test_session",
        role="user",
        content="Test content",
        ip_address="127.0.0.1"
    )
    
    db_session.add(message)
    await db_session.commit()
    await db_session.refresh(message)
    
    repr_str = repr(message)
    assert "ChatMessage" in repr_str
    assert "test_session" in repr_str
    assert "user" in repr_str
    assert str(message.id) in repr_str


@pytest.mark.asyncio
async def test_multiple_sessions(db_session):
    """Test handling multiple chat sessions."""
    sessions = ["session_a", "session_b", "session_c"]
    
    # Create messages for each session
    for session_id in sessions:
        for i in range(3):
            message = ChatMessage(
                session_id=session_id,
                role="user" if i % 2 == 0 else "assistant",
                content=f"Message {i} in {session_id}",
                ip_address="192.168.1.1"
            )
            db_session.add(message)
    
    await db_session.commit()
    
    # Verify each session has 3 messages
    for session_id in sessions:
        result = await db_session.execute(
            select(ChatMessage).where(ChatMessage.session_id == session_id)
        )
        messages = result.scalars().all()
        assert len(messages) == 3


@pytest.mark.asyncio
async def test_timestamp_ordering(db_session):
    """Test that messages can be ordered by timestamp."""
    import asyncio
    
    # Create messages with slight delays
    for i in range(5):
        message = ChatMessage(
            session_id="test_session",
            role="user" if i % 2 == 0 else "assistant",
            content=f"Message {i}",
            ip_address="192.168.1.1"
        )
        db_session.add(message)
        await db_session.commit()
        await asyncio.sleep(0.01)  # Small delay to ensure different timestamps
    
    # Query messages ordered by timestamp
    result = await db_session.execute(
        select(ChatMessage)
        .where(ChatMessage.session_id == "test_session")
        .order_by(ChatMessage.timestamp.asc())
    )
    messages = result.scalars().all()
    
    # Verify ordering
    assert len(messages) == 5
    for i in range(len(messages) - 1):
        assert messages[i].timestamp <= messages[i + 1].timestamp
