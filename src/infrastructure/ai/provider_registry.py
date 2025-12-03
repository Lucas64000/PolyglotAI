"""
AI Provider Registry

Single source of truth for AI provider registration.
Each provider registers both its configuration and factory together,
ensuring consistency and eliminating duplication.

This follows the Open/Closed Principle: adding a new provider requires
only creating new files with the @register decorator, without modifying
existing code.

Architecture:
    ┌─────────────────────────────────────────────────────────┐
    │                   AIProviderRegistry                     │
    │  ┌─────────────────────────────────────────────────────┐ │
    │  │  "azure" → ProviderEntry(                           │ │
    │  │              config_class=AzureOpenAIConfig,        │ │
    │  │              factory_class=AzureAIProviderFactory   │ │
    │  │           )                                         │ │
    │  │  "openai" → ProviderEntry(...)                      │ │
    │  │  "ollama" → ProviderEntry(...)                      │ │
    │  └─────────────────────────────────────────────────────┘ │
    └─────────────────────────────────────────────────────────┘

Usage:
    # In factory module - register both config and factory
    @AIProviderRegistry.register("azure", AzureOpenAIConfig)
    class AzureAIProviderFactory:
        def __init__(self, config: AzureOpenAIConfig) -> None:
            ...

    # In composition root - get factory with auto-loaded config
    factory = AIProviderRegistry.create_factory("azure")
    chat_model = factory.create_chat_model()
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Type

# Runtime types that accept Any to avoid Protocol __init__ issues with Pylance
# At runtime, these are Type[AIProviderConfig] and Type[AIProviderFactory]
ConfigClass = Type[Any]
FactoryClass = Type[Any]


@dataclass(frozen=True, slots=True)
class ProviderEntry:
    """
    Immutable entry linking a config class to its factory class.
    
    Attributes:
        config_class: The configuration class (e.g., AzureOpenAIConfig)
        factory_class: The factory class (e.g., AzureAIProviderFactory)
    """
    config_class: ConfigClass
    factory_class: FactoryClass


class AIProviderRegistry:
    """
    Central registry for AI providers.
    
    Ensures that each provider has both a config and factory registered
    together, preventing mismatches and forgotten registrations.
    
    Thread-safe for reads after module import (registration happens at import time).
    
    Principles:
        - Single Responsibility: Only manages provider registration/resolution
        - Open/Closed: New providers register via decorator, no code changes needed
        - Dependency Inversion: Depends on abstract AIProviderConfig/AIProviderFactory
    """
    
    _providers: dict[str, ProviderEntry] = {}
    
    @classmethod
    def register(
        cls,
        provider_name: str,
        config_class: ConfigClass,
    ) -> Callable[[FactoryClass], FactoryClass]:
        """
        Decorator to register a factory with its configuration class.
        
        This is the ONLY way to register a provider, ensuring config and
        factory are always registered together.
        
        Args:
            provider_name: Unique identifier (e.g., "azure", "openai", "ollama")
            config_class: The configuration class for this provider
            
        Returns:
            Decorator that registers the factory class
            
        Example:
            @AIProviderRegistry.register("azure", AzureOpenAIConfig)
            class AzureAIProviderFactory:
                def __init__(self, config: AzureOpenAIConfig) -> None:
                    self._config = config
                    
                def create_chat_model(self, ...) -> ChatModel:
                    ...
        
        Raises:
            ValueError: If provider_name is already registered (prevents accidents)
        """
        name = provider_name.lower()
        
        def decorator(factory_class: FactoryClass) -> FactoryClass:
            if name in cls._providers:
                existing = cls._providers[name]
                raise ValueError(
                    f"Provider '{name}' is already registered with "
                    f"factory={existing.factory_class.__name__}. "
                    f"Each provider can only be registered once."
                )
            
            cls._providers[name] = ProviderEntry(
                config_class=config_class,
                factory_class=factory_class,
            )
            return factory_class
        
        return decorator
    
    @classmethod
    def get_config_class(cls, provider_name: str) -> ConfigClass:
        """
        Get the configuration class for a provider.
        
        Args:
            provider_name: Provider identifier
            
        Returns:
            Configuration class
            
        Raises:
            ValueError: If provider is not registered
        """
        entry = cls._get_entry(provider_name)
        return entry.config_class
    
    @classmethod
    def get_factory_class(cls, provider_name: str) -> FactoryClass:
        """
        Get the factory class for a provider.
        
        Args:
            provider_name: Provider identifier
            
        Returns:
            Factory class
            
        Raises:
            ValueError: If provider is not registered
        """
        entry = cls._get_entry(provider_name)
        return entry.factory_class
    
    @classmethod
    def create_factory(cls, provider_name: str) -> Any:
        """
        Create a fully configured factory for a provider.
        
        This is a convenience method that:
        1. Gets the config class for the provider
        2. Loads config from environment via from_env()
        3. Creates and returns the factory with that config
        
        Args:
            provider_name: Provider identifier
            
        Returns:
            Configured factory instance ready to create AI components
            
        Raises:
            ValueError: If provider is not registered
            ConfigurationError: If config validation fails
            
        Example:
            factory = AIProviderRegistry.create_factory("azure")
            chat = factory.create_chat_model()
            embedder = factory.create_embedder()
        """
        entry = cls._get_entry(provider_name)
        config = entry.config_class.from_env()
        return entry.factory_class(config)
    
    @classmethod
    def create_factory_with_config(
        cls,
        provider_name: str,
        config: Any,
    ) -> Any:
        """
        Create a factory with a pre-loaded configuration.
        
        Use this when you already have a config instance
        (e.g., from dependency injection or testing).
        
        Args:
            provider_name: Provider identifier
            config: Pre-validated configuration instance
            
        Returns:
            Configured factory instance
            
        Raises:
            ValueError: If provider is not registered
            TypeError: If config type doesn't match expected type
        """
        entry = cls._get_entry(provider_name)
        
        # Validate config type matches
        if not isinstance(config, entry.config_class):
            raise TypeError(
                f"Config type mismatch for provider '{provider_name}': "
                f"expected {entry.config_class.__name__}, "
                f"got {type(config).__name__}"
            )
        
        return entry.factory_class(config)
    
    @classmethod
    def list_providers(cls) -> list[str]:
        """
        List all registered provider names.
        
        Returns:
            Sorted list of provider names
        """
        return sorted(cls._providers.keys())
    
    @classmethod
    def is_registered(cls, provider_name: str) -> bool:
        """
        Check if a provider is registered.
        
        Args:
            provider_name: Provider identifier
            
        Returns:
            True if registered, False otherwise
        """
        return provider_name.lower() in cls._providers
    
    @classmethod
    def _get_entry(cls, provider_name: str) -> ProviderEntry:
        """
        Get registry entry for a provider.
        
        Args:
            provider_name: Provider identifier
            
        Returns:
            ProviderEntry with config and factory classes
            
        Raises:
            ValueError: If provider is not registered
        """
        name = provider_name.lower()
        
        if name not in cls._providers:
            available = ", ".join(cls.list_providers()) or "none"
            raise ValueError(
                f"Unknown AI provider: '{provider_name}'. "
                f"Available providers: {available}. "
                f"Make sure the provider module is imported."
            )
        
        return cls._providers[name]
    
    @classmethod
    def clear(cls) -> None:
        """
        Clear all registrations.
        
        WARNING: Only use in tests! This breaks the singleton-like
        behavior of the registry.
        """
        cls._providers.clear()
