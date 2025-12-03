"""
Azure Embedder

Embedder implementation for Azure OpenAI Service.
"""

from .base_openai_embedder import BaseOpenAIEmbedder

from openai import AsyncAzureOpenAI


class AzureEmbedder(BaseOpenAIEmbedder):
    """
    Embedder implementation for Azure OpenAI.
    """
    
    def __init__(
        self,
        api_key: str,
        endpoint: str,
        api_version: str,
        deployment_name: str,
    ) -> None:
        """
        Initialize Azure embedder.
        
        Args:
            api_key: Azure OpenAI API key
            endpoint: Azure OpenAI endpoint URL
            api_version: API version
            deployment_name: Azure embedding deployment name
        """
        super().__init__(
            model_name=deployment_name,
        )
        self._api_key = api_key
        self._endpoint = endpoint
        self._api_version = api_version
    
    def _create_client(self) -> AsyncAzureOpenAI:
        """Create Azure OpenAI async client."""
        from openai import AsyncAzureOpenAI
        
        return AsyncAzureOpenAI(
            api_key=self._api_key,
            azure_endpoint=self._endpoint,
            api_version=self._api_version,
        )
