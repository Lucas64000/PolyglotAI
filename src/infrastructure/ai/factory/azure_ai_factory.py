"""
Azure AI Provider Factory

Concrete factory for creating Azure OpenAI components.
"""

from src.core.ports.driven import ChatModel, Embedder
from src.infrastructure.ai.provider_registry import AIProviderRegistry
from src.infrastructure.config.ai import AzureOpenAIConfig


@AIProviderRegistry.register("azure", AzureOpenAIConfig)
class AzureAIProviderFactory:
    """
    Factory for Azure OpenAI components.
    
    Creates ChatModel and Embedder instances configured for Azure OpenAI.
    
    Requires AzureOpenAIConfig which validates:
    - AZURE_OPENAI_API_KEY (required)
    - AZURE_OPENAI_ENDPOINT (required)
    - AZURE_OPENAI_API_VERSION
    - AZURE_OPENAI_CHAT_DEPLOYMENT (required)
    - AZURE_OPENAI_EMBEDDING_DEPLOYMENT (required)
    """
    
    def __init__(self, config: AzureOpenAIConfig) -> None:
        """
        Initialize with Azure OpenAI configuration.

        Args:
            config: Azure OpenAI configuration (pre-validated)
        """
        self._config = config
        # Extract secret once at initialization
        self._api_key = config.api_key.get_secret_value()
    
    @property
    def provider_name(self) -> str:
        """Get the provider name."""
        return "azure"
    
    def create_chat_model(
        self,
        model_name: str | None = None,
        temperature: float | None = None,
        max_tokens: int | None = None,
    ) -> ChatModel:
        """
        Create an Azure-configured chat model.
        
        Args:
            model_name: Deployment name override.
                       If None, uses default from config.
            temperature: Sampling temperature. If None, uses config default.
            max_tokens: Maximum response tokens. If None, uses config default.
            
        Returns:
            AzureChatModel instance
        """
        from src.infrastructure.ai.chat import AzureChatModel
        
        return AzureChatModel(
            api_key=self._api_key,
            endpoint=self._config.endpoint,
            api_version=self._config.api_version,
            deployment_name=model_name or self._config.chat_deployment,
            temperature=temperature if temperature is not None else self._config.defaults.temperature,
            max_tokens=max_tokens if max_tokens is not None else self._config.defaults.max_tokens,
        )
    
    def create_embedder(
        self,
        model_name: str | None = None,
    ) -> Embedder:
        """
        Create an Azure-configured embedder.
        
        Args:
            model_name: Deployment name override.
                       If None, uses default from config.
            
        Returns:
            AzureEmbedder instance
        """
        from src.infrastructure.ai.embeddings import AzureEmbedder
        
        return AzureEmbedder(
            api_key=self._api_key,
            endpoint=self._config.endpoint,
            api_version=self._config.api_version,
            deployment_name=model_name or self._config.embedding_deployment,
        )
