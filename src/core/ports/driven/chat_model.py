"""
ChatModel Port

Interface for LLM chat completion services.
This is what services use to generate responses.
"""

from abc import abstractmethod
from typing import Any, Protocol

from ...domain.entities import ChatMessage


class ChatModel(Protocol):
    """
    Interface for chat-based language model interactions.
    
    This Protocol defines how the application layer communicates
    with LLM services, regardless of the underlying provider
    (Azure, OpenAI, Ollama, etc.).
    
    All methods are async for optimal I/O handling.
    
    Usage:
        ```python
        # Injected via DI, provider-agnostic
        async def tutor_respond(chat_model: ChatModel, messages: list[ChatMessage]) -> str:
            response = await chat_model.generate(messages)
            return response
        ```
    """
    
    @property
    @abstractmethod
    def model_name(self) -> str:
        """Get the name of the model being used."""
        ...
    
    @abstractmethod
    async def generate(
        self,
        messages: list[ChatMessage],
    ) -> str:
        """
        Generate a text response from the conversation history.
        
        Args:
            messages: List of ChatMessage objects representing the conversation
            
        Returns:
            Generated text response
            
        Raises:
            LLMError: If the API call fails
            LLMResponseError: If the response is empty or invalid
        """
        ...
    
    @abstractmethod
    async def generate_json(
        self,
        messages: list[ChatMessage],
    ) -> dict[str, Any]:
        """
        Generate a JSON response from the conversation history.
        
        Uses the model's JSON mode to ensure valid JSON output.
        
        Args:
            messages: List of ChatMessage objects representing the conversation
            
        Returns:
            Parsed JSON response as a dictionary
            
        Raises:
            LLMError: If the API call fails
            LLMResponseError: If the response is empty or invalid
            LLMJSONDecodeError: If the response is not valid JSON
        """
        ...
    
    @abstractmethod
    async def generate_with_metadata(
        self,
        messages: list[ChatMessage],
    ) -> tuple[str, dict[str, Any]]:
        """
        Generate a response with additional metadata.
        
        Returns both the response text and metadata like:
        - Token usage
        - Response ID
        - Finish reason
        
        Args:
            messages: List of ChatMessage objects
            
        Returns:
            Tuple of (response_text, metadata_dict)
        """
        ...