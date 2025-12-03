"""
Azure Chat Model

ChatModel implementation for Azure OpenAI Service.
"""

from .base_openai_chat import BaseOpenAIChatModel

from openai import AsyncAzureOpenAI


class AzureChatModel(BaseOpenAIChatModel):
    """
    ChatModel implementation for Azure OpenAI.
    
    Uses AsyncAzureOpenAI client for async operations.
    """
    
    def __init__(
        self,
        api_key: str,
        endpoint: str,
        api_version: str,
        deployment_name: str,
        temperature: float = 0.7,
        max_tokens: int = 1024,
    ) -> None:
        """
        Initialize Azure chat model.
        
        Args:
            api_key: Azure OpenAI API key
            endpoint: Azure OpenAI endpoint URL
            api_version: API version 
            deployment_name: Azure deployment name
            temperature: Sampling temperature
            max_tokens: Maximum response tokens
        """
        super().__init__(
            model_name=deployment_name,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        self._api_key = api_key
        self._endpoint = endpoint
        self._api_version = api_version
    
    def _create_client(self) -> AsyncAzureOpenAI:
        """Create Azure OpenAI async client."""
        return AsyncAzureOpenAI(
            api_key=self._api_key,
            azure_endpoint=self._endpoint,
            api_version=self._api_version,
        )
