
from typing import Protocol

from src.core.domain.entities import ChatMessage


class LLMClient(Protocol):
    """
    Protocol for LLM clients.
    
    Each implementation handles message format conversion internally,
    allowing support for different API formats (OpenAI, Anthropic, Gemini, etc.)
    without exposing format-specific types.
    """

    async def generate(
        self,
        messages: tuple[ChatMessage, ...],
        system_prompt: str,
    ) -> str:
        """
        Generate a response from the LLM.
        
        Args:
            messages: Conversation history as domain entities.
            system_prompt: System instructions for the LLM.
            
        Returns:
            The generated response text.
        """
        ...