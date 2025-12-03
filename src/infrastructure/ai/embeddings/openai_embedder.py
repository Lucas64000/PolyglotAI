"""
OpenAI Embedder

Embedder implementation for OpenAI API.
"""

from .base_openai_embedder import BaseOpenAIEmbedder

from openai import AsyncOpenAI


class OpenAIEmbedder(BaseOpenAIEmbedder):
    """
    Embedder implementation for OpenAI API.
    """
    
    def __init__(
        self,
        api_key: str,
        model_name: str,
    ) -> None:
        """
        Initialize OpenAI embedder.
        
        Args:
            api_key: OpenAI API key
            model_name: Embedding model name
            dimensions: Optional dimension override
        """
        super().__init__(
            model_name=model_name,
        )
        self._api_key = api_key
    
    def _create_client(self) -> AsyncOpenAI:
        """Create OpenAI async client."""
        from openai import AsyncOpenAI
        
        return AsyncOpenAI(
            api_key=self._api_key,
        )
