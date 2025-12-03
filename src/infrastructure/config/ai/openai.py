"""
OpenAI Configuration

Configuration for the OpenAI API provider.
"""

from typing import ClassVar, Self

from pydantic import model_validator

from src.core.exceptions import ConfigurationError
from src.infrastructure.config.base import (
    SecretString,
    get_env,
    require_env,
)
from src.infrastructure.config.ai.base import (
    AIProviderConfig,
    LLMDefaults,
    ProviderType,
)


class OpenAIConfig(AIProviderConfig):
    """
    OpenAI API configuration.
    
    Required environment variables:
    - OPENAI_API_KEY: Your OpenAI API key
    
    Optional environment variables:
    - OPENAI_CHAT_MODEL: Chat model (default: gpt-4o-mini)
    - OPENAI_EMBEDDING_MODEL: Embedding model (default: text-embedding-3-small)
    
    YAML section: providers.openai
    """
    
    provider_name: ClassVar[ProviderType] = "openai"
    yaml_section: ClassVar[tuple[str, ...]] = ("providers", "openai")
    
    api_key: SecretString
    chat_model: str = "gpt-4o-mini"
    embedding_model: str = "text-embedding-3-small"
    
    @property
    def is_cloud(self) -> bool:
        return True
    
    @property
    def requires_api_key(self) -> bool:
        return True
    
    def get_chat_model(self) -> str:
        """Get the chat model name."""
        return self.chat_model
    
    def get_embedding_model(self) -> str:
        """Get the embedding model name."""
        return self.embedding_model
    
    @model_validator(mode="after")
    def _validate_api_key(self) -> Self:
        """Ensure API key is set and not empty."""
        if not self.api_key:
            raise ConfigurationError(
                "OpenAI API key is required but not set",
                config_key="OPENAI_API_KEY"
            )
        return self
    
    @classmethod
    def from_env(cls) -> Self:
        """
        Create OpenAI config from environment variables.
        
        Loads defaults from YAML, then overrides with env vars.
        
        Returns:
            Validated OpenAI configuration
        
        Raises:
            ConfigurationError: If required OPENAI_API_KEY is not set
        """
        yaml_defaults = cls._get_yaml_values()
        
        # Load LLM defaults from YAML if present
        llm_yaml = yaml_defaults.get("defaults", {})
        defaults = LLMDefaults(
            temperature=float(get_env("LLM_TEMPERATURE", str(llm_yaml.get("temperature", 0.7))) or 0.7),
            max_tokens=int(get_env("LLM_MAX_TOKENS", str(llm_yaml.get("max_tokens", 1024))) or 1024),
            timeout=float(get_env("LLM_TIMEOUT", str(llm_yaml.get("timeout", 60.0))) or 60.0),
            max_retries=int(get_env("LLM_MAX_RETRIES", str(llm_yaml.get("max_retries", 3))) or 3),
        )
        
        return cls(
            api_key=SecretString(require_env("OPENAI_API_KEY")),
            chat_model=get_env("OPENAI_CHAT_MODEL", yaml_defaults.get("chat_model", "gpt-4o-mini")) or "gpt-4o-mini",
            embedding_model=get_env("OPENAI_EMBEDDING_MODEL", yaml_defaults.get("embedding_model", "text-embedding-3-small")) or "text-embedding-3-small",
            defaults=defaults,
        )
