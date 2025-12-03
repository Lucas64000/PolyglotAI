"""
Azure OpenAI Configuration

Configuration for the Azure OpenAI Service provider.
"""

from typing import ClassVar, Self

from pydantic import field_validator, model_validator

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


class AzureOpenAIConfig(AIProviderConfig):
    """
    Azure OpenAI Service configuration.
    
    Required environment variables:
    - AZURE_OPENAI_API_KEY: Your Azure OpenAI API key
    - AZURE_OPENAI_ENDPOINT: Your Azure OpenAI endpoint URL
    - AZURE_OPENAI_CHAT_DEPLOYMENT: Deployment name for chat model
    - AZURE_OPENAI_EMBEDDING_DEPLOYMENT: Deployment name for embedding model
    
    Optional environment variables:
    - AZURE_OPENAI_API_VERSION: API version 
    
    YAML section: providers.azure
    
    Note:
        The actual model is determined by the deployment configuration in Azure.
    """
    
    provider_name: ClassVar[ProviderType] = "azure"
    yaml_section: ClassVar[tuple[str, ...]] = ("providers", "azure")
    
    api_key: SecretString
    endpoint: str
    api_version: str = "2025-01-01-preview"
    chat_deployment: str
    embedding_deployment: str
    
    @property
    def is_cloud(self) -> bool:
        return True
    
    @property
    def requires_api_key(self) -> bool:
        return True
    
    def get_chat_model(self) -> str:
        """Azure uses deployment names as model identifiers."""
        return self.chat_deployment
    
    def get_embedding_model(self) -> str:
        """Azure uses deployment names as model identifiers."""
        return self.embedding_deployment
    
    @field_validator("endpoint")
    @classmethod
    def _validate_endpoint(cls, v: str) -> str:
        """Ensure endpoint is a valid HTTPS URL."""
        if not v.startswith("https://"):
            raise ConfigurationError(
                "Azure OpenAI endpoint must be an HTTPS URL",
                config_key="AZURE_OPENAI_ENDPOINT"
            )
        # Normalize: remove trailing slash
        return v.rstrip("/")
    
    @model_validator(mode="after")
    def _validate_required_fields(self) -> Self:
        """Validate all required fields are set and not empty."""
        required: dict[str, object] = {
            "AZURE_OPENAI_API_KEY": self.api_key,
            "AZURE_OPENAI_ENDPOINT": self.endpoint,
            "AZURE_OPENAI_CHAT_DEPLOYMENT": self.chat_deployment,
            "AZURE_OPENAI_EMBEDDING_DEPLOYMENT": self.embedding_deployment,
        }
        missing = [key for key, value in required.items() if not value]
        
        if missing:
            raise ConfigurationError(
                f"Missing required Azure configuration: {', '.join(missing)}",
                config_key="azure"
            )
        return self
    
    @classmethod
    def from_env(cls) -> Self:
        """
        Create Azure OpenAI config from environment variables.
        
        Loads defaults from YAML, then overrides with env vars.
        
        Returns:
            Validated Azure OpenAI configuration
        
        Raises:
            ConfigurationError: If required environment variables are not set
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
            api_key=SecretString(require_env("AZURE_OPENAI_API_KEY")),
            endpoint=require_env("AZURE_OPENAI_ENDPOINT"),
            api_version=get_env("AZURE_OPENAI_API_VERSION", yaml_defaults.get("api_version", "2025-01-01-preview")) or "2025-01-01-preview",
            chat_deployment=require_env("AZURE_OPENAI_CHAT_DEPLOYMENT"),
            embedding_deployment=require_env("AZURE_OPENAI_EMBEDDING_DEPLOYMENT"),
            defaults=defaults,
        )
