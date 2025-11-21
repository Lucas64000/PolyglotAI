
from abc import ABC, abstractmethod

from typing import Generic
from src.core.types import TMessage, TResponse

from ..clients.config.config_interface import ClientConfig
from ..clients.client_interface import ClientWrapper
from ..adapters.adapter_interface import MessageAdapter
from ..providers.provider_interface import BaseLLMProvider

class BaseLLMBuilder(Generic[TMessage, TResponse], ABC):
    """
    Interface pour un constructeur de provider LLM.
    """

    def build(
        self, 
        model_name: str, 
        temperature: float,
        max_tokens: int,
    ) -> BaseLLMProvider[TMessage, TResponse]:
        """
        Construit et retourne une instance complète du provider LLM
        (en assemblant ClientConfig, ClientWrapper, Adapter et Provider).
        """
        client_config = self._build_client_config(model_name=model_name)
        client_wrapper = self._build_client(client_config=client_config)
        adapter = self._build_adapter()
        provider = self._build_provider(
            model_name=model_name,
            client_wrapper=client_wrapper,
            adapter=adapter,
            temperature=temperature,
            max_tokens=max_tokens,
        )

        return provider
    
    @abstractmethod
    def _build_client_config(self, model_name: str) -> ClientConfig:
        pass

    @abstractmethod
    def _build_client(self, client_config: ClientConfig) -> ClientWrapper[TMessage, TResponse]:
        pass

    @abstractmethod
    def _build_adapter(self) -> MessageAdapter[TMessage, TResponse]:
        pass

    @abstractmethod
    def _build_provider(
        self,
        model_name: str,
        client_wrapper: ClientWrapper[TMessage, TResponse],
        adapter: MessageAdapter[TMessage, TResponse],
        temperature: float,
        max_tokens: int,
    ) -> BaseLLMProvider[TMessage, TResponse]:
        """Assemble le provider final avec tous ses composants."""
        pass