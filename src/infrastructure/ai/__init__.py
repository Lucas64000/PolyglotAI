"""
AI Infrastructure Module

Contains implementations for AI providers:
- AIProviderRegistry: Central registry for provider config+factory pairs
- Factory implementations (Abstract Factory pattern)
- Chat model implementations
- Embedder implementations

To add a new provider:
1. Create config class in src/infrastructure/config/ai/
2. Create factory class in src/infrastructure/ai/factory/
3. Decorate factory with @AIProviderRegistry.register("name", ConfigClass)
4. Import factory in src/infrastructure/ai/factory/__init__.py

That's it! No need to modify settings.py or any other files.
"""

from .provider_registry import AIProviderRegistry

# Import factory module to trigger registrations
from . import factory  # noqa: F401

# Re-export commonly used classes
from .factory import (
    AzureAIProviderFactory,
    OpenAIProviderFactory,
    OllamaProviderFactory,
)
from .chat import AzureChatModel, OpenAIChatModel, OllamaChatModel
from .embeddings import AzureEmbedder, OpenAIEmbedder, OllamaEmbedder

__all__ = [
    # Registry
    "AIProviderRegistry",
    # Factories
    "AzureAIProviderFactory",
    "OpenAIProviderFactory",
    "OllamaProviderFactory",
    # Chat Models
    "AzureChatModel",
    "OpenAIChatModel",
    "OllamaChatModel",
    # Embedders
    "AzureEmbedder",
    "OpenAIEmbedder",
    "OllamaEmbedder",
]
