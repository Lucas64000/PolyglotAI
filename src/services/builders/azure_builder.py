
from src.utils.logger import get_logger
from src.utils.config import get_config

from openai.types.chat import ChatCompletionMessageParam, ChatCompletion

from .builder_interface import BaseLLMBuilder
from .builder_registry import BuilderRegistry

from src.clients.config.config_interface import ClientConfig
from src.clients.config.azure_config import AzureClientConfig

from src.clients.client_interface import ClientWrapper
from src.clients.azure_client import AzureClientWrapper

from src.adapters.llm_adapter.adapter_interface import MessageAdapter
from src.adapters.llm_adapter.openai_adapter import OpenAIMessageAdapter 

from src.services.service_interface import BaseLLMService
from src.services.azure_service import AzureLLMService


logger = get_logger(__name__)


@BuilderRegistry.register("azure")
class AzureLLMBuilder(BaseLLMBuilder[ChatCompletionMessageParam, ChatCompletion]):
    """
    Builder spécifique pour Azure OpenAI.
    Implémente les étapes de construction propres à Azure.
    """

    def build(self, model_name: str, temperature: float, max_tokens: int) -> BaseLLMService[ChatCompletionMessageParam, ChatCompletion]:
        return super().build(model_name, temperature, max_tokens)

    def _build_client_config(self, model_name: str) -> AzureClientConfig:
        """
        Construit la configuration Azure depuis les variables d'environnement
        """
        logger.debug(f"Construction de la config Azure pour : {model_name}")
        config = get_config()
        service_config = config.get_service_config("azure")
        extra = service_config.get("extra", {})
        try:
            return AzureClientConfig(
                api_key=config.get_env("AZURE_OPENAI_API_KEY"),
                azure_endpoint=config.get_env("AZURE_OPENAI_ENDPOINT"),
                azure_deployment=model_name,
                api_version=service_config.get("api_version", "2025-01-01-preview"),
                timeout=extra.get("timeout"),
                max_retries=extra.get("max_retries")
            )
        except (ValueError, KeyError) as e:
            logger.error(f"Configuration Azure incomplète: {e}")
            raise ValueError(f"Configuration Azure incomplète: {e}") from e


    def _build_client(self, client_config: ClientConfig) -> ClientWrapper[ChatCompletionMessageParam, ChatCompletion]:
        """
        Crée le wrapper client Azure OpenAI
        """
        if not isinstance(client_config, AzureClientConfig):
            raise TypeError(f"Expected AzureClientConfig, got {type(client_config)}")
        
        logger.debug("Création du client Azure OpenAI")
        return AzureClientWrapper(config=client_config)

    def _build_adapter(self) -> MessageAdapter[ChatCompletionMessageParam, ChatCompletion]:
        """
        Crée l'adaptateur de messages OpenAI
        """
        logger.debug("Création de l'adaptateur OpenAI")
        return OpenAIMessageAdapter()

    def _build_service(
        self,
        model_name: str,
        client_wrapper: ClientWrapper[ChatCompletionMessageParam, ChatCompletion],
        adapter: MessageAdapter[ChatCompletionMessageParam, ChatCompletion],
        temperature: float,
        max_tokens: int,
    ) -> BaseLLMService[ChatCompletionMessageParam, ChatCompletion]:
        """
        Assemble le service Azure LLM final
        """
        logger.debug("Assemblage du service Azure LLM")
        return AzureLLMService(
            model_name=model_name,
            client=client_wrapper,
            adapter=adapter,
            temperature=temperature,
            max_tokens=max_tokens,
        )
