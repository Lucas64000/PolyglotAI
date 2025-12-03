"""OpenAI Provider Factory

Concrete factory for creating OpenAI components.
"""

from src.core.ports.driven import ChatModel, Embedder
from src.infrastructure.ai.provider_registry import AIProviderRegistry
from src.infrastructure.config.ai import OpenAIConfig


@AIProviderRegistry.register("openai", OpenAIConfig)
class OpenAIProviderFactory:
    """
    Factory for OpenAI components.
    
    Creates ChatModel and Embedder instances configured for OpenAI API.
    
    Requires OpenAIConfig which validates:
    - OPENAI_API_KEY (required)
    - OPENAI_CHAT_MODEL (default: gpt-4o-mini)
    - OPENAI_EMBEDDING_MODEL (default: text-embedding-3-small)
    """
    
    def __init__(self, config: OpenAIConfig) -> None:
        """
        Initialize with OpenAI configuration.
        
        Args:
            config: OpenAI configuration (pre-validated)
        """
        self._config = config
        # Extract secret once at initialization
        self._api_key = config.api_key.get_secret_value()
    
    @property
    def provider_name(self) -> str:
        """Get the provider name."""
        return "openai"
    
    def create_chat_model(
        self,
        model_name: str | None = None,
        temperature: float | None = None,
        max_tokens: int | None = None,
    ) -> ChatModel:
        """
        Create an OpenAI-configured chat model.
        
        Args:
            model_name: Model name override (e.g., "gpt-4o", "gpt-4o-mini").
                       If None, uses default from config.
            temperature: Sampling temperature. If None, uses config default.
            max_tokens: Maximum response tokens. If None, uses config default.
            
        Returns:
            OpenAIChatModel instance
        """
        from src.infrastructure.ai.chat import OpenAIChatModel
        
        return OpenAIChatModel(
            api_key=self._api_key,
            model_name=model_name or self._config.chat_model,
            temperature=temperature if temperature is not None else self._config.defaults.temperature,
            max_tokens=max_tokens if max_tokens is not None else self._config.defaults.max_tokens,
        )
    
    def create_embedder(
        self,
        model_name: str | None = None,
    ) -> Embedder:
        """
        Create an OpenAI-configured embedder.
        
        Args:
            model_name: Model name override.
                       If None, uses default from config.
            
        Returns:
            OpenAIEmbedder instance
        """
        from src.infrastructure.ai.embeddings import OpenAIEmbedder
        
        return OpenAIEmbedder(
            api_key=self._api_key,
            model_name=model_name or self._config.embedding_model,
        )
