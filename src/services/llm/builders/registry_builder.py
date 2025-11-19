
from typing import Dict, Type, Callable, Any

from .builder_interface import BaseLLMBuilder

class BuilderRegistry:
    """
    Registre central pour les builders métier LLM.
    
    Permet :
        - l'enregistrement des builders LLM (Azure, OpenAI, etc.)
        - la récupération dynamique d'un service par son nom
        - lister tous les builders enregistrés
    """

    # Mapping du nom du service vers la classe concrète LLMService
    _builders: Dict[str, Type[BaseLLMBuilder[Any, Any]]] = {}

    @classmethod
    def register(cls, builder_name: str) -> Callable[[Type[BaseLLMBuilder[Any, Any]]], Type[BaseLLMBuilder[Any, Any]]]:
        """
        Décorateur pour enregistrer un service LLM dans le registre.
        
        Args:
            builder_name: Nom unique du service (ex: "azure", "openai")
        
        Returns:
            Décorateur qui enregistre la classe du service dans le registre.
        
        Exemple :
            @BuilderRegistry.register("azure")
            class AzureLLMBuilder(BaseLLMBuilder):
                ...
        """
        def decorator(service_cls: Type[BaseLLMBuilder[Any, Any]]) -> Type[BaseLLMBuilder[Any, Any]]:
            cls._builders[builder_name] = service_cls
            return service_cls

        return decorator

    @classmethod
    def get(cls, builder_name: str) -> Type[BaseLLMBuilder[Any, Any]]:
        """
        Récupère un service LLM par son nom.
        
        Args:
            builder_name: Nom du service enregistré
        
        Returns:
            Classe concrète du service LLM
        
        Raises:
            KeyError si le service n'est pas enregistré
        """
        if builder_name not in cls._builders:
            available_builders = ", ".join(cls._builders.keys()) or "aucun"
            raise KeyError(
                f"Service LLM '{builder_name}' non enregistré. "
                f"builders disponibles : {available_builders}"
            )
        return cls._builders[builder_name]

    @classmethod
    def list(cls) -> list[str]:
        """
        Retourne la liste de tous les builders LLM enregistrés.
        
        Returns:
            Liste des noms des builders enregistrés
        """
        return list(cls._builders.keys())
