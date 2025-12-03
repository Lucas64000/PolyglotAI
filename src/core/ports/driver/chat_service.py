"""
ChatService Port

Interface for the chat service.
This is what the API layer calls to process user messages.
"""

from abc import abstractmethod
from typing import Protocol
from uuid import UUID

from ...domain.entities import ChatMessage, LearningSession


class ChatService(Protocol):
    """
    Interface for the conversational tutoring service.
    
    This is the main entry point for conversation interactions.
    The API calls this interface; the application layer implements it.  
    """
    
    @abstractmethod
    async def start_session(
        self,
        user_id: UUID,
        focus_topic: str | None = None,
    ) -> LearningSession:
        """
        Start a new learning session.
        
        Args:
            user_id: The user's unique identifier
            focus_topic: Optional topic to focus on
            
        Returns:
            New LearningSession instance
        """
        ...
    
    @abstractmethod
    async def process_message(
        self,
        session_id: UUID,
        user_message: str,
    ) -> ChatMessage:
        """
        Process a user message and generate a tutor response.
        
        Args:
            session_id: The current session's identifier
            user_message: The user's input text
            
        Returns:
            ChatMessage containing the tutor's response
            
        Raises:
            SessionNotActiveError: If session is ended
            EntityNotFoundError: If session doesn't exist
        """
        ...
    
    @abstractmethod
    async def get_session(
        self,
        session_id: UUID,
    ) -> LearningSession | None:
        """
        Retrieve a session by ID.
        
        Args:
            session_id: The session's identifier
            
        Returns:
            LearningSession if found, None otherwise
        """
        ...
    
    @abstractmethod
    async def end_session(
        self,
        session_id: UUID,
    ) -> LearningSession:
        """
        End an active session.
        
        Args:
            session_id: The session's identifier
            
        Returns:
            The ended session
            
        Raises:
            EntityNotFoundError: If session doesn't exist
        """
        ...
    
    @abstractmethod
    async def get_session_history(
        self,
        session_id: UUID,
    ) -> list[ChatMessage]:
        """
        Get all messages from a session.
        
        Args:
            session_id: The session's identifier
            
        Returns:
            List of messages in chronological order
        """
        ...
