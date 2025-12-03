"""
AI Provider Configuration Package

Contains configuration classes for each supported AI provider.
Each provider has its own module with validation specific to that provider.

Note:
    Registration of providers is handled via AIProviderRegistry in
    src/infrastructure/ai/provider_registry.py. The factories import
    and register their associated configs.
"""

from .base import AIProviderConfig, LLMDefaults, ProviderType
from .azure import AzureOpenAIConfig
from .ollama import OllamaConfig
from .openai import OpenAIConfig

__all__ = [
    "AIProviderConfig",
    "AzureOpenAIConfig",
    "LLMDefaults",
    "OllamaConfig",
    "OpenAIConfig",
    "ProviderType",
]
