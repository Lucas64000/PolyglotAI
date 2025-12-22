"""
Chat Provider

Interface for chat completion services.
This is what services use to generate responses.
"""

from typing import Protocol

from src.core.domain.entities import ChatMessage
from src.core.domain.value_objects import TutorProfile 

class ChatProvider(Protocol):
    """
    Port for generative conversational services.
    
    This interface abstracts the interaction with any text generation mechanism. 
    """
    
    async def generate_response(
        self,
        history: tuple[ChatMessage, ...],
        tutor_profile: TutorProfile,
    ) -> str:
        """
        Generate a pedagogical response based on conversation history and tutor personality.

        Args:
            history: Chronological list of conversation messages.
            tutor_profile: Configuration object defining the tutor's tone and behavior.
            
        Returns:
            The generated text response content.
            
        Raises:
            TutorGenerationError: If the external service fails or returns invalid content.
        """
        ...