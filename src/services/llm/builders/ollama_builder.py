
from src.utils.logger import get_logger
from src.utils.config import get_config

from openai.types.chat import ChatCompletionMessageParam, ChatCompletion

from .openai_builder import OpenAILLMBuilder
from .registry_builder import BuilderRegistry

from ..clients.config.config_interface import ClientConfig
from ..clients.config.ollama_config import OllamaClientConfig

from ..clients.client_interface import ClientWrapper
from ..clients.ollama_client import OllamaClientWrapper


logger = get_logger(__name__)


@BuilderRegistry.register("ollama")
class OllamaLLMBuilder(OpenAILLMBuilder):
    """
    Builder spécifique pour Ollama OpenAI.
    Implémente les étapes de construction propres à Ollama.
    """

    def _build_client_config(self, model_name: str) -> OllamaClientConfig:
        """
        Construit la configuration Ollama depuis les variables d'environnement
        """
        logger.debug(f"Construction de la config Ollama pour : {model_name}")
        config = get_config()
        provider_config = config.get_provider_config("ollama")
        extra = provider_config.get("extra", {})
        try:
            return OllamaClientConfig(
                base_url=provider_config.get("base_url", ""),
                timeout=extra.get("timeout"),
                max_retries=extra.get("max_retries")
            )
        except (ValueError, KeyError) as e:
            logger.error(f"Configuration Ollama incomplète: {e}")
            raise ValueError(f"Configuration Ollama incomplète: {e}") from e


    def _build_client(self, client_config: ClientConfig) -> ClientWrapper[ChatCompletionMessageParam, ChatCompletion]:
        """
        Crée le wrapper client Ollama OpenAI
        """
        if not isinstance(client_config, OllamaClientConfig):
            raise TypeError(f"Expected OllamaClientConfig, got {type(client_config)}")
        
        logger.debug("Création du client Ollama OpenAI")
        return OllamaClientWrapper(config=client_config)