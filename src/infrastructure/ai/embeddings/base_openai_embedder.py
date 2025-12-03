"""
Base OpenAI Embedder

Shared implementation for OpenAI-compatible embedding models.
"""

from abc import ABC, abstractmethod

from openai import AsyncOpenAI, AsyncAzureOpenAI
from openai.types.create_embedding_response import CreateEmbeddingResponse

from src.core.exceptions.ai_exceptions import EmbeddingError, EmbeddingResponseError


class BaseOpenAIEmbedder(ABC):
    """
    Base class for OpenAI-compatible embedding models.
    
    Provides shared implementation for embedding generation.
    Subclasses must implement _create_client().
    """

    def __init__(
        self,
        model_name: str,
    ) -> None:
        """
        Initialize common parameters.
        
        Args:
            model_name: Embedding model name
        """
        self._model_name = model_name
        self._client: AsyncOpenAI | AsyncAzureOpenAI | None = None
    
    @property
    def model_name(self) -> str:
        """Get the model name."""
        return self._model_name
    
    @abstractmethod
    def _create_client(self) -> AsyncOpenAI | AsyncAzureOpenAI:
        """Create the appropriate async client."""
        ...
    
    @property
    def client(self) -> AsyncOpenAI | AsyncAzureOpenAI:
        """Get or create the client (lazy initialization)."""
        if self._client is None:
            self._client = self._create_client()
        return self._client
    
    async def _embed_raw(self, input_data: str | list[str]) -> CreateEmbeddingResponse:
        """
        Internal method to generate raw embedding API response.
        
        Args:
            input_data: Text or list of texts to embed
            
        Returns:
            Raw CreateEmbeddingResponse from OpenAI SDK
            
        Raises:
            EmbeddingError: If API call fails
        """
        try:
            response = await self.client.embeddings.create(
                model=self._model_name,
                input=input_data,
            )
        except Exception as e:
            raise EmbeddingError("openai", f"API call failed: {e}", e) from e
        
        return response
    
    async def embed(self, text: str) -> list[float]:
        """
        Generate embedding for a single text.
        
        Args:
            text: Text to embed
            
        Returns:
            Embedding vector as list of floats
            
        Raises:
            EmbeddingResponseError: If response is empty
        """
        response = await self._embed_raw(text)
        
        if not response.data:
            raise EmbeddingResponseError("openai", "Empty embedding response")
        
        return response.data[0].embedding
    
    async def embed_batch(self, texts: list[str]) -> list[list[float]]:
        """
        Generate embeddings for multiple texts.
        
        More efficient than calling embed() multiple times.
        
        Args:
            texts: List of texts to embed
            
        Returns:
            List of embedding vectors
            
        Raises:
            EmbeddingResponseError: If response is empty
        """
        if not texts:
            return []
        
        response = await self._embed_raw(texts)
        
        if not response.data:
            raise EmbeddingResponseError("openai", "Empty embedding response")

        # Sort by index to maintain order
        sorted_data = sorted(response.data, key=lambda x: x.index)
        return [item.embedding for item in sorted_data]
