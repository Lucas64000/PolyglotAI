"""
Chat Provider

Interface for chat completion services.
This is what services use to get teacher responses.
"""

from typing import Protocol

from src.core.domain.entities import ChatMessage
from src.core.domain.value_objects import TeacherProfile 

class ChatProvider(Protocol):
    """
    Port for conversational services.
    
    This interface abstracts the interaction with any text response mechanism. 
    """
    
    async def get_teacher_response(
        self,
        history: tuple[ChatMessage, ...],
        teacher_profile: TeacherProfile,
    ) -> str:
        """
        Get a pedagogical response from the teacher based on conversation history and teacher personality.

        Args:
            history: Chronological list of conversation messages.
            teacher_profile: Configuration object defining the teacher's tone and behavior.
            
        Returns:
            The teacher's response content.
            
        Raises:
            TeacherGenerationError: If the external service fails or returns invalid content.
        """
        ...