"""
OpenAI Chat Model

ChatModel implementation for OpenAI API.
"""

from .base_openai_chat import BaseOpenAIChatModel

from openai import AsyncOpenAI


class OpenAIChatModel(BaseOpenAIChatModel):
    """
    ChatModel implementation for OpenAI API.
    
    Uses AsyncOpenAI client for async operations.
    """
    
    def __init__(
        self,
        api_key: str,
        model_name: str,
        temperature: float = 0.7,
        max_tokens: int = 1024,
    ) -> None:
        """
        Initialize OpenAI chat model.
        
        Args:
            api_key: OpenAI API key
            model_name: Model name 
            temperature: Sampling temperature
            max_tokens: Maximum response tokens
        """
        super().__init__(
            model_name=model_name,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        self._api_key = api_key
    
    def _create_client(self) -> AsyncOpenAI:
        """Create OpenAI async client."""
        from openai import AsyncOpenAI
        
        return AsyncOpenAI(
            api_key=self._api_key,
        )
