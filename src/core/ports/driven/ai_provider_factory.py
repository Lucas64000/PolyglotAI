"""
AIProviderFactory Port

Abstract Factory interface for creating families of AI components.
- If config says "azure", ALL components (chat, embeddings) are Azure
- If config says "openai", ALL components are OpenAI
... 

The factory is created once at startup in the Composition Root,
and injected wherever AI components are needed.
"""

from abc import abstractmethod
from typing import Protocol

from .chat_model import ChatModel
from .embedder import Embedder


class AIProviderFactory(Protocol):
    """
    Abstract Factory for creating consistent AI provider components.
    
    This Protocol ensures that all AI components (chat model, embedder)
    come from the same provider, preventing configuration inconsistencies.
    """
    
    @property
    @abstractmethod
    def provider_name(self) -> str:
        """
        Get the name of this provider.
        
        Returns:
            Provider identifier (e.g., "azure")
        """
        ...
    
    @abstractmethod
    def create_chat_model(
        self,
        model_name: str | None = None,
        temperature: float = 0.7,
        max_tokens: int = 1024,
    ) -> ChatModel:
        """
        Create a chat model for conversational AI.
        
        Args:
            model_name: Model/deployment name override.
                       If None, uses the default from config.
            temperature: Sampling temperature (0.0-2.0)
            max_tokens: Maximum tokens in response
            
        Returns:
            ChatModel instance configured for this provider
            
        Raises:
            ConfigurationError: If model is not available
        """
        ...
    
    @abstractmethod
    def create_embedder(
        self,
        model_name: str | None = None,
    ) -> Embedder:
        """
        Create an embedder for text embeddings.
        
        Args:
            model_name: Model/deployment name override.
                       If None, uses the default from config.
        
        Returns:
            Embedder instance configured for this provider

        Raises:
            ConfigurationError: If model is not available
        """
        ...
