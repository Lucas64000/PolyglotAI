
from typing import Any

from .builders.builder_registry import BuilderRegistry
from .service_interface import BaseLLMService

from src.utils.logger import get_logger
from src.utils.config import get_config

logger = get_logger(__name__)

class LLMFacade:
    """
    Façade pour la création de services LLM.
    """

    @staticmethod
    def create_llm_service(
        service_name: str,
        model_name: str,
        temperature: float,
        max_tokens: int = 1000
    ) -> BaseLLMService[Any, Any]:
        """
        Crée et retourne une instance de service LLM prête à l'emploi.

        Args:
            service_name: Nom du fournisseur
            model_name: Nom du modèle 

        Returns:
            Une instance d'un service LLM configuré.
        """

        logger.info(
            f"Demande de création de service LLM : provider={service_name}, "
            f"model={model_name}, temperature={temperature}"
        )

        try:
            # On récupère le builder depuis le registre
            builder = BuilderRegistry.get(service_name)()
        except KeyError:
            available = BuilderRegistry.list()
            logger.error(f"Aucun builder trouvé pour le provider: '{service_name}'. "
                         f"Builders disponibles: {available}")
            raise ValueError(f"Provider '{service_name}' non supporté.")

        # Le builder construit le service
        try:
            service = builder.build(
                model_name=model_name,
                temperature=temperature,
                max_tokens=max_tokens,
            )
            logger.info(f"Service LLM pour '{service_name}' créé avec succès.")
            return service
        except Exception as e:
            logger.error(f"Échec de la construction du service par le builder '{service_name}': {e}")
            raise

from src.models.conversation_model import Message
from src.core.enums import Role

if __name__ == "__main__":
    config = get_config()
    service_name = config.service_default
    model_name = config.model_name_default
    temperature = config.temperature_default
    max_tokens = config.max_tokens_default
    
    service = LLMFacade.create_llm_service(
        service_name=service_name,
        model_name=model_name,
        temperature=temperature,
        max_tokens=max_tokens
    )

    message = Message(role=Role.USER, content="Hello World!")
    response = service.generate([message])

    print()
    print(message.content)
    print(response.content)
