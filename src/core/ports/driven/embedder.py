"""
Embedder Port

Interface for text embedding services.
Used by any RAG components.
"""

from abc import abstractmethod
from typing import Protocol


class Embedder(Protocol):
    """
    Interface for text embedding generation.
    
    Embeddings are vector representations of text used for:
    - Semantic search in the knowledge graph
    - Similarity matching between concepts
    - RAG (Retrieval Augmented Generation)
    
    This interface allows swapping embedding providers.
    
    All methods are async for optimal I/O handling.
    """
    
    @property
    @abstractmethod
    def model_name(self) -> str:
        """Get the name of the embedding model being used."""
        ...
    
    @abstractmethod
    async def embed(self, text: str) -> list[float]:
        """
        Generate an embedding for a single text.
        
        Args:
            text: The text to embed
            
        Returns:
            List of floats representing the embedding vector
            
        Raises:
            EmbeddingError: If the API call fails
        """
        ...
    
    @abstractmethod
    async def embed_batch(self, texts: list[str]) -> list[list[float]]:
        """
        Generate embeddings for multiple texts efficiently.
        
        More efficient than calling embed() multiple times
        due to batching at the API level.
        
        Args:
            texts: List of texts to embed
            
        Returns:
            List of embedding vectors, one per input text
            
        Raises:
            EmbeddingError: If the API call fails
        """
        ...
