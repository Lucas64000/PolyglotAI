"""
AI Provider Factory Module

Contains the Abstract Factory implementations for creating
consistent AI provider components.

To add a new provider:
1. Create a new factory file (e.g., anthropic_ai_factory.py)
2. Decorate with @AIProviderRegistry.register("name", ConfigClass)
3. Import the module here to trigger registration

No need to modify settings.py or any other files!
"""

from src.infrastructure.ai.provider_registry import AIProviderRegistry

# Import factory modules to trigger registration
from .azure_ai_factory import AzureAIProviderFactory
from .openai_ai_factory import OpenAIProviderFactory
from .ollama_ai_factory import OllamaProviderFactory

__all__ = [
    "AIProviderRegistry",
    "AzureAIProviderFactory",
    "OpenAIProviderFactory",
    "OllamaProviderFactory",
]
