"""Repository for chat message database operations."""

from typing import List, Optional
from sqlalchemy import select, delete, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError

from ..models.chat_message import ChatMessage


class ChatRepository:
    """
    Repository for managing chat message persistence.
    
    Provides async methods for saving messages, retrieving chat history,
    and deleting chat sessions with proper error handling.
    """
    
    def __init__(self, db_session: AsyncSession):
        """
        Initialize repository with database session.
        
        Args:
            db_session: SQLAlchemy async session for database operations
        """
        self.db_session = db_session
    
    async def save_message(
        self,
        session_id: str,
        role: str,
        content: str,
        ip_address: Optional[str] = None
    ) -> ChatMessage:
        """
        Save a chat message to the database.
        
        Args:
            session_id: Unique identifier for the chat session
            role: Message sender role ('user' or 'assistant')
            content: The message text content
            ip_address: Optional IP address of the user
            
        Returns:
            ChatMessage: The saved message with generated ID and timestamp
            
        Raises:
            SQLAlchemyError: If database operation fails
        """
        try:
            message = ChatMessage(
                session_id=session_id,
                role=role,
                content=content,
                ip_address=ip_address
            )
            
            self.db_session.add(message)
            await self.db_session.flush()
            await self.db_session.refresh(message)
            
            return message
            
        except SQLAlchemyError as e:
            await self.db_session.rollback()
            raise SQLAlchemyError(f"Failed to save message: {str(e)}") from e
    
    async def get_history(
        self,
        session_id: str,
        limit: int = 50
    ) -> List[ChatMessage]:
        """
        Retrieve chat history for a session.
        
        Args:
            session_id: Unique identifier for the chat session
            limit: Maximum number of messages to retrieve (default 50, max 100)
            
        Returns:
            List[ChatMessage]: Messages ordered by timestamp ascending
            
        Raises:
            SQLAlchemyError: If database operation fails
        """
        try:
            # Enforce maximum limit of 100
            limit = min(limit, 100)
            
            # Query messages for session, ordered by timestamp
            stmt = (
                select(ChatMessage)
                .where(ChatMessage.session_id == session_id)
                .order_by(ChatMessage.timestamp.asc())
                .limit(limit)
            )
            
            result = await self.db_session.execute(stmt)
            messages = result.scalars().all()
            
            return list(messages)
            
        except SQLAlchemyError as e:
            raise SQLAlchemyError(f"Failed to retrieve chat history: {str(e)}") from e
    
    async def delete_session(self, session_id: str) -> int:
        """
        Delete all messages for a chat session.
        
        Args:
            session_id: Unique identifier for the chat session
            
        Returns:
            int: Number of messages deleted
            
        Raises:
            SQLAlchemyError: If database operation fails
        """
        try:
            # First count the messages to be deleted
            count_stmt = (
                select(func.count())
                .select_from(ChatMessage)
                .where(ChatMessage.session_id == session_id)
            )
            result = await self.db_session.execute(count_stmt)
            count = result.scalar() or 0
            
            # Delete all messages for the session
            delete_stmt = (
                delete(ChatMessage)
                .where(ChatMessage.session_id == session_id)
            )
            await self.db_session.execute(delete_stmt)
            await self.db_session.flush()
            
            return count
            
        except SQLAlchemyError as e:
            await self.db_session.rollback()
            raise SQLAlchemyError(f"Failed to delete session: {str(e)}") from e
