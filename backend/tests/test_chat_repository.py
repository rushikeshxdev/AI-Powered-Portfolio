"""Tests for ChatRepository."""

import pytest
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.exc import SQLAlchemyError

from src.models.chat_message import ChatMessage, Base
from src.repositories.chat_repository import ChatRepository


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


@pytest.fixture
def chat_repository(db_session):
    """Create a ChatRepository instance with test database session."""
    return ChatRepository(db_session)


@pytest.mark.asyncio
async def test_save_message_with_all_fields(chat_repository, db_session):
    """Test saving a message with all required fields."""
    # Save a message
    message = await chat_repository.save_message(
        session_id="test_session_123",
        role="user",
        content="What projects has Rushikesh worked on?",
        ip_address="192.168.1.1"
    )
    
    await db_session.commit()
    
    # Verify the message was saved correctly
    assert message.id is not None
    assert message.session_id == "test_session_123"
    assert message.role == "user"
    assert message.content == "What projects has Rushikesh worked on?"
    assert message.ip_address == "192.168.1.1"
    assert message.timestamp is not None


@pytest.mark.asyncio
async def test_save_message_without_ip_address(chat_repository, db_session):
    """Test saving a message without IP address (optional field)."""
    # Save a message without IP address
    message = await chat_repository.save_message(
        session_id="test_session",
        role="assistant",
        content="This is a response",
        ip_address=None
    )
    
    await db_session.commit()
    
    # Verify the message was saved
    assert message.id is not None
    assert message.ip_address is None
    assert message.content == "This is a response"


@pytest.mark.asyncio
async def test_save_multiple_messages(chat_repository, db_session):
    """Test saving multiple messages in sequence."""
    # Save multiple messages
    message1 = await chat_repository.save_message(
        session_id="session_1",
        role="user",
        content="Question 1",
        ip_address="192.168.1.1"
    )
    
    message2 = await chat_repository.save_message(
        session_id="session_1",
        role="assistant",
        content="Answer 1",
        ip_address="192.168.1.1"
    )
    
    await db_session.commit()
    
    # Verify both messages were saved
    assert message1.id is not None
    assert message2.id is not None
    assert message1.id != message2.id


@pytest.mark.asyncio
async def test_get_history_basic(chat_repository, db_session):
    """Test retrieving chat history for a session."""
    # Create test messages
    await chat_repository.save_message(
        session_id="session_1",
        role="user",
        content="Question 1",
        ip_address="192.168.1.1"
    )
    
    await chat_repository.save_message(
        session_id="session_1",
        role="assistant",
        content="Answer 1",
        ip_address="192.168.1.1"
    )
    
    await chat_repository.save_message(
        session_id="session_2",
        role="user",
        content="Different session",
        ip_address="192.168.1.2"
    )
    
    await db_session.commit()
    
    # Retrieve history for session_1
    history = await chat_repository.get_history("session_1")
    
    # Verify results
    assert len(history) == 2
    assert history[0].role == "user"
    assert history[0].content == "Question 1"
    assert history[1].role == "assistant"
    assert history[1].content == "Answer 1"


@pytest.mark.asyncio
async def test_get_history_with_limit(chat_repository, db_session):
    """Test retrieving chat history with pagination limit."""
    # Create 10 messages
    for i in range(10):
        await chat_repository.save_message(
            session_id="test_session",
            role="user" if i % 2 == 0 else "assistant",
            content=f"Message {i}",
            ip_address="192.168.1.1"
        )
    
    await db_session.commit()
    
    # Retrieve with limit of 5
    history = await chat_repository.get_history("test_session", limit=5)
    
    # Verify only 5 messages returned
    assert len(history) == 5
    assert history[0].content == "Message 0"
    assert history[4].content == "Message 4"


@pytest.mark.asyncio
async def test_get_history_enforces_max_limit(chat_repository, db_session):
    """Test that get_history enforces maximum limit of 100."""
    # Create 150 messages
    for i in range(150):
        await chat_repository.save_message(
            session_id="test_session",
            role="user",
            content=f"Message {i}",
            ip_address="192.168.1.1"
        )
    
    await db_session.commit()
    
    # Try to retrieve with limit > 100
    history = await chat_repository.get_history("test_session", limit=150)
    
    # Verify only 100 messages returned (max limit)
    assert len(history) == 100


@pytest.mark.asyncio
async def test_get_history_default_limit(chat_repository, db_session):
    """Test that get_history uses default limit of 50."""
    # Create 75 messages
    for i in range(75):
        await chat_repository.save_message(
            session_id="test_session",
            role="user",
            content=f"Message {i}",
            ip_address="192.168.1.1"
        )
    
    await db_session.commit()
    
    # Retrieve without specifying limit
    history = await chat_repository.get_history("test_session")
    
    # Verify default limit of 50 is applied
    assert len(history) == 50


@pytest.mark.asyncio
async def test_get_history_ordered_by_timestamp(chat_repository, db_session):
    """Test that messages are returned in chronological order."""
    import asyncio
    
    # Create messages with slight delays
    for i in range(5):
        await chat_repository.save_message(
            session_id="test_session",
            role="user",
            content=f"Message {i}",
            ip_address="192.168.1.1"
        )
        await db_session.commit()
        await asyncio.sleep(0.01)  # Small delay to ensure different timestamps
    
    # Retrieve history
    history = await chat_repository.get_history("test_session")
    
    # Verify chronological order
    assert len(history) == 5
    for i in range(len(history) - 1):
        assert history[i].timestamp <= history[i + 1].timestamp


@pytest.mark.asyncio
async def test_get_history_empty_session(chat_repository, db_session):
    """Test retrieving history for a session with no messages."""
    # Retrieve history for non-existent session
    history = await chat_repository.get_history("nonexistent_session")
    
    # Verify empty list returned
    assert len(history) == 0
    assert history == []


@pytest.mark.asyncio
async def test_delete_session_basic(chat_repository, db_session):
    """Test deleting all messages for a session."""
    # Create messages for two sessions
    await chat_repository.save_message(
        session_id="session_1",
        role="user",
        content="Message 1",
        ip_address="192.168.1.1"
    )
    
    await chat_repository.save_message(
        session_id="session_1",
        role="assistant",
        content="Message 2",
        ip_address="192.168.1.1"
    )
    
    await chat_repository.save_message(
        session_id="session_2",
        role="user",
        content="Different session",
        ip_address="192.168.1.2"
    )
    
    await db_session.commit()
    
    # Delete session_1
    deleted_count = await chat_repository.delete_session("session_1")
    await db_session.commit()
    
    # Verify correct count returned
    assert deleted_count == 2
    
    # Verify session_1 messages are gone
    history_1 = await chat_repository.get_history("session_1")
    assert len(history_1) == 0
    
    # Verify session_2 messages still exist
    history_2 = await chat_repository.get_history("session_2")
    assert len(history_2) == 1


@pytest.mark.asyncio
async def test_delete_session_returns_count(chat_repository, db_session):
    """Test that delete_session returns the correct count of deleted messages."""
    # Create 5 messages
    for i in range(5):
        await chat_repository.save_message(
            session_id="test_session",
            role="user",
            content=f"Message {i}",
            ip_address="192.168.1.1"
        )
    
    await db_session.commit()
    
    # Delete the session
    deleted_count = await chat_repository.delete_session("test_session")
    await db_session.commit()
    
    # Verify count
    assert deleted_count == 5


@pytest.mark.asyncio
async def test_delete_nonexistent_session(chat_repository, db_session):
    """Test deleting a session that doesn't exist."""
    # Delete non-existent session
    deleted_count = await chat_repository.delete_session("nonexistent_session")
    await db_session.commit()
    
    # Verify count is 0
    assert deleted_count == 0


@pytest.mark.asyncio
async def test_delete_session_multiple_times(chat_repository, db_session):
    """Test deleting the same session multiple times."""
    # Create messages
    await chat_repository.save_message(
        session_id="test_session",
        role="user",
        content="Message",
        ip_address="192.168.1.1"
    )
    
    await db_session.commit()
    
    # Delete first time
    count1 = await chat_repository.delete_session("test_session")
    await db_session.commit()
    assert count1 == 1
    
    # Delete second time (should return 0)
    count2 = await chat_repository.delete_session("test_session")
    await db_session.commit()
    assert count2 == 0


@pytest.mark.asyncio
async def test_repository_with_different_roles(chat_repository, db_session):
    """Test repository handles both user and assistant roles correctly."""
    # Save messages with different roles
    user_msg = await chat_repository.save_message(
        session_id="test_session",
        role="user",
        content="User question",
        ip_address="192.168.1.1"
    )
    
    assistant_msg = await chat_repository.save_message(
        session_id="test_session",
        role="assistant",
        content="Assistant response",
        ip_address="192.168.1.1"
    )
    
    await db_session.commit()
    
    # Verify both roles saved correctly
    assert user_msg.role == "user"
    assert assistant_msg.role == "assistant"
    
    # Retrieve and verify
    history = await chat_repository.get_history("test_session")
    assert len(history) == 2
    assert history[0].role == "user"
    assert history[1].role == "assistant"
