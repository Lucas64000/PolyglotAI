"""
Ollama Chat Model

ChatModel implementation for Ollama (local LLM with OpenAI-compatible API).
"""

from .base_openai_chat import BaseOpenAIChatModel

from openai import AsyncOpenAI


class OllamaChatModel(BaseOpenAIChatModel):
    """
    ChatModel implementation for Ollama local LLM.
    
    Ollama provides an OpenAI-compatible API at /v1/,
    so we reuse the OpenAI SDK with a custom base_url.
    """
    
    def __init__(
        self,
        base_url: str,
        model_name: str,
        temperature: float = 0.7,
        max_tokens: int = 1024,
    ) -> None:
        """
        Initialize Ollama chat model.
        
        Args:
            base_url: Ollama server URL
            model_name: Model name
            temperature: Sampling temperature
            max_tokens: Maximum response tokens
        """
        super().__init__(
            model_name=model_name,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        # Ensure base_url ends with /v1 for OpenAI compatibility
        self._base_url = base_url.rstrip("/")
        if not self._base_url.endswith("/v1"):
            self._base_url = f"{self._base_url}/v1"
    
    def _create_client(self) -> AsyncOpenAI:
        """Create OpenAI-compatible async client for Ollama."""
        from openai import AsyncOpenAI
        
        return AsyncOpenAI(
            base_url=self._base_url,
            api_key="ollama",  # Ollama doesn't require an API key
        )
