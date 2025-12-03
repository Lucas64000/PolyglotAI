"""Ollama Provider Factory

Concrete factory for creating Ollama components (local LLM).
"""

from src.core.ports.driven import ChatModel, Embedder
from src.infrastructure.ai.provider_registry import AIProviderRegistry
from src.infrastructure.config.ai import OllamaConfig


@AIProviderRegistry.register("ollama", OllamaConfig)
class OllamaProviderFactory:
    """
    Factory for Ollama components (local LLM).
    
    Creates ChatModel and Embedder instances configured for Ollama.
    Ollama runs locally, so no API key is needed.
    
    Requires OllamaConfig which provides:
    - OLLAMA_BASE_URL (default: http://localhost:11434)
    - OLLAMA_CHAT_MODEL (default: qwen2.5:7b)
    - OLLAMA_EMBEDDING_MODEL (default: nomic-embed-text)
    """
    
    def __init__(self, config: OllamaConfig) -> None:
        """
        Initialize with Ollama configuration.
        
        Args:
            config: Ollama configuration
        """
        self._config = config
    
    @property
    def provider_name(self) -> str:
        """Get the provider name."""
        return "ollama"
    
    def create_chat_model(
        self,
        model_name: str | None = None,
        temperature: float | None = None,
        max_tokens: int | None = None,
    ) -> ChatModel:
        """
        Create an Ollama-configured chat model.
        
        Args:
            model_name: Model name override (e.g., "qwen2.5:7b", "mistral").
                       If None, uses default from config.
            temperature: Sampling temperature. If None, uses config default.
            max_tokens: Maximum response tokens. If None, uses config default.
            
        Returns:
            OllamaChatModel instance
        """
        from src.infrastructure.ai.chat import OllamaChatModel
        
        return OllamaChatModel(
            base_url=self._config.openai_compatible_url,
            model_name=model_name or self._config.chat_model,
            temperature=temperature if temperature is not None else self._config.defaults.temperature,
            max_tokens=max_tokens if max_tokens is not None else self._config.defaults.max_tokens,
        )
    
    def create_embedder(
        self,
        model_name: str | None = None,
    ) -> Embedder:
        """
        Create an Ollama-configured embedder.
        
        Args:
            model_name: Model name override (e.g., "nomic-embed-text", "mxbai-embed-large").
                       If None, uses default from config.
            
        Returns:
            OllamaEmbedder instance
        """
        from src.infrastructure.ai.embeddings import OllamaEmbedder
        
        return OllamaEmbedder(
            base_url=self._config.openai_compatible_url,
            model_name=model_name or self._config.embedding_model,
        )
