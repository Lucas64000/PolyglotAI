
from abc import ABC, abstractmethod

from typing import Generic
from src.core.types import TMessage, TResponse

from src.clients.config.config_interface import ClientConfig
from src.clients.client_interface import ClientWrapper
from src.adapters.llm_adapter.adapter_interface import MessageAdapter
from ..service_interface import BaseLLMService

class BaseLLMBuilder(Generic[TMessage, TResponse], ABC):
    """
    Interface pour un constructeur de service LLM.
    """

    def build(
        self, 
        model_name: str, 
        temperature: float,
        max_tokens: int,
    ) -> BaseLLMService[TMessage, TResponse]:
        """
        Construit et retourne une instance complète du service LLM
        (en assemblant ClientConfig, ClientWrapper, Adapter et Service).
        """
        client_config = self._build_client_config(model_name=model_name)
        client_wrapper = self._build_client(client_config=client_config)
        adapter = self._build_adapter()
        service = self._build_service(
            model_name=model_name,
            client_wrapper=client_wrapper,
            adapter=adapter,
            temperature=temperature,
            max_tokens=max_tokens,
        )

        return service
    
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
    def _build_service(
        self,
        model_name: str,
        client_wrapper: ClientWrapper[TMessage, TResponse],
        adapter: MessageAdapter[TMessage, TResponse],
        temperature: float,
        max_tokens: int,
    ) -> BaseLLMService[TMessage, TResponse]:
        """Assemble le service final avec tous ses composants."""
        pass