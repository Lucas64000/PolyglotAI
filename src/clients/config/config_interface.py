
from abc import ABC, abstractmethod
from typing import Dict, Any

class ClientConfig(ABC):
    """
    Interface pour toutes les configurations LLM
    Vérifie la configuration une fois créée
    """

    def __post_init__(self) -> None:
        self.validate()

    @abstractmethod
    def to_sdk_kwargs(self) -> Dict[str, Any]:
        """Retourne les paramètres formatés pour le SDK du provider."""
        pass
    
    @abstractmethod
    def validate(self) -> None:
        """
        Permet de valider la config.
        """
        return
    

