"""
Ollama Configuration

Configuration for the Ollama local LLM provider.
"""

from __future__ import annotations

from typing import ClassVar, Self

from pydantic import field_validator, model_validator

from src.core.exceptions import ConfigurationError
from src.infrastructure.config.base import get_env
from src.infrastructure.config.ai.base import (
    AIProviderConfig,
    LLMDefaults,
    ProviderType,
)


class OllamaConfig(AIProviderConfig):
    """
    Ollama local LLM configuration.
    
    Optional environment variables:
    - OLLAMA_BASE_URL: Ollama server URL (default: http://localhost:11434)
    - OLLAMA_CHAT_MODEL: Chat model (default: qwen2.5:7b)
    - OLLAMA_EMBEDDING_MODEL: Embedding model (default: nomic-embed-text)
    
    YAML section: providers.ollama
    
    Note:
        Ollama runs locally so no API key is required.
        Ensure Ollama is running and the models are pulled before use.
    """
    
    provider_name: ClassVar[ProviderType] = "ollama"
    yaml_section: ClassVar[tuple[str, ...]] = ("providers", "ollama")
    
    base_url: str = "http://localhost:11434"
    chat_model: str = "qwen2.5:7b"
    embedding_model: str = "nomic-embed-text"
    
    @property
    def is_cloud(self) -> bool:
        return False
    
    @property
    def requires_api_key(self) -> bool:
        return False
    
    def get_chat_model(self) -> str:
        """Get the chat model name."""
        return self.chat_model
    
    def get_embedding_model(self) -> str:
        """Get the embedding model name."""
        return self.embedding_model
    
    @field_validator("base_url")
    @classmethod
    def _validate_base_url(cls, v: str) -> str:
        """Ensure base_url is a valid HTTP(S) URL."""
        if not v.startswith(("http://", "https://")):
            raise ConfigurationError(
                "Ollama base URL must be an HTTP or HTTPS URL",
                config_key="OLLAMA_BASE_URL"
            )
        # Normalize: remove trailing slash
        return v.rstrip("/")
    
    @property
    def openai_compatible_url(self) -> str:
        """Get the OpenAI-compatible API endpoint."""
        return f"{self.base_url}/v1"
    
    @model_validator(mode="after")
    def _validate_required_fields(self) -> Self:
        """Validate all required fields are set and not empty."""
        required: dict[str, object] = {
            "OLLAMA_BASE_URL": self.base_url,
            "OLLAMA_CHAT_MODEL": self.chat_model,
            "OLLAMA_EMBEDDING_MODEL": self.embedding_model,
        }
        missing = [key for key, value in required.items() if not value]
        
        if missing:
            raise ConfigurationError(
                f"Missing required Ollama configuration: {', '.join(missing)}",
                config_key="ollama"
            )
        return self
    
    @classmethod
    def from_env(cls) -> Self:
        """
        Create Ollama config from environment variables.
        
        Loads defaults from YAML, then overrides with env vars.
        
        Returns:
            Validated Ollama configuration
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
            base_url=get_env("OLLAMA_BASE_URL", yaml_defaults.get("base_url", "http://localhost:11434")) or "http://localhost:11434",
            chat_model=get_env("OLLAMA_CHAT_MODEL", yaml_defaults.get("chat_model", "qwen2.5:7b")) or "qwen2.5:7b",
            embedding_model=get_env("OLLAMA_EMBEDDING_MODEL", yaml_defaults.get("embedding_model", "nomic-embed-text")) or "nomic-embed-text",
            defaults=defaults,
        )
