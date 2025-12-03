"""
Ollama Embedder

Embedder implementation for Ollama (local LLM with OpenAI-compatible API).
"""

from .base_openai_embedder import BaseOpenAIEmbedder

from openai import AsyncOpenAI


class OllamaEmbedder(BaseOpenAIEmbedder):
    """
    Embedder implementation for Ollama local embedding models.
    
    Ollama provides an OpenAI-compatible API at /v1/,
    so we reuse the OpenAI SDK with a custom base_url.
    """
    
    def __init__(
        self,
        base_url: str,
        model_name: str = "nomic-embed-text",
    ) -> None:
        """
        Initialize Ollama embedder.
        
        Args:
            base_url: Ollama server URL
            model_name: Embedding model name 
        """
        super().__init__(
            model_name=model_name,
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
