
from typing import Any

from src.services.llm.builders.registry_builder import BuilderRegistry
from src.services.llm.providers.provider_interface import BaseLLMProvider

from src.utils.logger import get_logger

logger = get_logger(__name__)

class LLMFactory:
    """
    Factory pour la création de providers de LLM.
    """

    @staticmethod
    def create_llm_provider(
        provider_name: str,
        model_name: str,
        temperature: float,
        max_tokens: int = 1000
    ) -> BaseLLMProvider[Any, Any]:
        """
        Crée et retourne une instance de provider LLM prête à l'emploi.

        Args:
            provider_name: Nom du fournisseur
            model_name: Nom du modèle 

        Returns:
            Une instance d'un provider LLM configuré.
        """

        logger.info(
            f"Demande de création de provider LLM : provider={provider_name}, "
            f"model={model_name}, temperature={temperature}"
        )

        try:
            # On récupère le builder depuis le registre
            builder = BuilderRegistry.get(provider_name)()
        except KeyError:
            available = BuilderRegistry.list()
            logger.error(f"Aucun builder trouvé pour le provider: '{provider_name}'. "
                         f"Builders disponibles: {available}")
            raise ValueError(f"Provider '{provider_name}' non supporté.")

        # Le builder construit le provider
        try:
            provider = builder.build(
                model_name=model_name,
                temperature=temperature,
                max_tokens=max_tokens,
            )
            logger.info(f"provider LLM pour '{provider_name}' créé avec succès.")
            return provider
        except Exception as e:
            logger.error(f"Échec de la construction du provider par le builder '{provider_name}': {e}")
            raise