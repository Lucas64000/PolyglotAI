
from src.utils.logger import get_logger
from src.utils.config import get_config

from openai.types.chat import ChatCompletionMessageParam, ChatCompletion

from .openai_builder import OpenAILLMBuilder
from .registry_builder import BuilderRegistry

from ..clients.config.config_interface import ClientConfig
from ..clients.config.azure_config import AzureClientConfig

from ..clients.client_interface import ClientWrapper
from ..clients.azure_client import AzureClientWrapper

logger = get_logger(__name__)

@BuilderRegistry.register("azure")
class AzureLLMBuilder(OpenAILLMBuilder):
    """
    Builder spécifique pour Azure OpenAI.
    Implémente les étapes de construction propres à Azure.
    """

    def _build_client_config(self, model_name: str) -> AzureClientConfig:
        """
        Construit la configuration Azure depuis les variables d'environnement
        """
        logger.debug(f"Construction de la config Azure pour : {model_name}")
        config = get_config()
        provider_config = config.get_provider_config("azure")
        extra = provider_config.get("extra", {})
        try:
            return AzureClientConfig(
                api_key=config.get_env("AZURE_OPENAI_API_KEY"),
                azure_endpoint=config.get_env("AZURE_OPENAI_ENDPOINT"),
                azure_deployment=model_name,
                api_version=provider_config.get("api_version", "2025-01-01-preview"),
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