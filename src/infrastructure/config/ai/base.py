"""
AI Provider Base Configuration

Defines the abstract base for all AI provider configurations.
Each provider must implement its own config class with proper validation.
"""

from abc import abstractmethod
from typing import ClassVar, Literal, Self

from src.infrastructure.config.base import (
    ImmutableConfig,
    YAMLConfigLoader,
)


# Type alias for provider names
ProviderType = Literal["openai", "azure", "ollama"]


class LLMDefaults(ImmutableConfig):
    """
    Default LLM parameters shared across all providers.
    
    These can be overridden per-request but provide sensible defaults.
    """
    
    temperature: float = 0.7
    max_tokens: int = 1024
    timeout: float = 60.0
    max_retries: int = 3


class AIProviderConfig(ImmutableConfig, YAMLConfigLoader):
    """
    Abstract base for AI provider configurations.
    
    Each provider must implement:
    - `from_env()`: Factory method to create from environment
    - `provider_name`: Class variable identifying the provider
    - `get_chat_model()`: Returns the chat model name
    - `get_embedding_model()`: Returns the embedding model name
    
    Common properties available on all providers:
    - `defaults`: LLM default parameters
    """
    
    provider_name: ClassVar[ProviderType]
    
    defaults: LLMDefaults = LLMDefaults()
    
    @classmethod
    @abstractmethod
    def from_env(cls) -> Self:
        """Create configuration from environment variables."""
        ...
    
    @property
    @abstractmethod
    def is_cloud(self) -> bool:
        """Whether this provider requires internet connectivity."""
        ...
    
    @property
    @abstractmethod
    def requires_api_key(self) -> bool:
        """Whether this provider requires an API key."""
        ...
    
    @abstractmethod
    def get_chat_model(self) -> str:
        """Get the chat model name/identifier."""
        ...
    
    @abstractmethod
    def get_embedding_model(self) -> str:
        """Get the embedding model name/identifier."""
        ...
