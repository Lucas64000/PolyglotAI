
from abc import ABC, abstractmethod
from typing import Dict, Any, List

class ClientConfig(ABC):
    """
    Interface pour toutes les configurations LLM
    Vérifie la configuration une fois créée
    """

    @abstractmethod
    def to_sdk_kwargs(self) -> Dict[str, Any]:
        """Retourne les paramètres formatés pour le SDK du provider."""
        pass
    
    def _validate(self, required_fields: List[str]) -> None:
        """Valide les champs requis et optionnels de la config"""
        for field in required_fields:
            value = getattr(self, field)
            if not value or not isinstance(value, str) or value.strip() == "":
                raise ValueError(f"Le champ requis '{field}' est vide ou invalide.")
        
        # Validation optionnelle pour timeout et max_retries si présents
        timeout = getattr(self, 'timeout', None)
        if timeout is not None and timeout <= 0:
            raise ValueError("Le champ 'timeout' doit être un nombre positif.")
        
        max_retries = getattr(self, 'max_retries', None)
        if max_retries is not None and max_retries < 0:
            raise ValueError("Le champ 'max_retries' doit être un entier positif ou zéro.")
