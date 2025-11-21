
from abc import ABC, abstractmethod

from src.services.llm.clients.config.config_interface import ClientConfig
from .builder_interface import BaseLLMBuilder
from openai.types.chat import ChatCompletionMessageParam, ChatCompletion

from src.utils.logger import get_logger

from ..adapters.adapter_interface import MessageAdapter
from ..adapters.openai_adapter import OpenAIMessageAdapter

from ..clients.client_interface import ClientWrapper

from ..providers.provider_interface import BaseLLMProvider
from ..providers.openai_provider import OpenAILLMProvider

logger = get_logger(__name__)

class OpenAILLMBuilder(BaseLLMBuilder[ChatCompletionMessageParam, ChatCompletion], ABC):

    @abstractmethod
    def _build_client_config(self, model_name: str) -> ClientConfig:
        pass
    
    @abstractmethod
    def _build_client(self, client_config: ClientConfig) -> ClientWrapper[ChatCompletionMessageParam, ChatCompletion]:
        pass

    def _build_adapter(self) -> MessageAdapter[ChatCompletionMessageParam, ChatCompletion]:
        """
        Crée l'adaptateur de messages OpenAI
        """
        logger.debug("Création de l'adaptateur OpenAI")
        return OpenAIMessageAdapter()

    def _build_provider(
        self,
        model_name: str,
        client_wrapper: ClientWrapper[ChatCompletionMessageParam, ChatCompletion],
        adapter: MessageAdapter[ChatCompletionMessageParam, ChatCompletion],
        temperature: float,
        max_tokens: int,
    ) -> BaseLLMProvider[ChatCompletionMessageParam, ChatCompletion]:
        """
        Assemble le provider OpenAI LLM final
        """
        logger.debug("Assemblage du provider OpenAI LLM")
        return OpenAILLMProvider(
            model_name=model_name,
            client=client_wrapper,
            adapter=adapter,
            temperature=temperature,
            max_tokens=max_tokens,
        )