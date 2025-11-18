from dataclasses import dataclass
from typing import Any, Dict
from .config_interface import ClientConfig

from src.utils.logger import get_logger

logger = get_logger(__name__)

@dataclass(frozen=True)
class AzureClientConfig(ClientConfig):
    api_key: str
    azure_endpoint: str
    azure_deployment: str
    api_version: str
    timeout: float | None = None        
    max_retries: int | None = None     

    def to_sdk_kwargs(self) -> Dict[str, Any]:
        kwargs: Dict[str, Any] = {
            "api_key": self.api_key,
            "azure_endpoint": self.azure_endpoint,
            "azure_deployment": self.azure_deployment,
            "api_version": self.api_version,
        }
        if self.timeout is not None:
            kwargs["timeout"] = self.timeout
        if self.max_retries is not None:
            kwargs["max_retries"] = self.max_retries
        return kwargs

    def validate(self) -> None:
        # Validation des clés requises pour Azure
        required_fields = ["api_key", "azure_endpoint", "azure_deployment", "api_version"]
        for field in required_fields:
            value = getattr(self, field)
            if not value or not isinstance(value, str) or value.strip() == "":
                raise ValueError(f"Le champ requis '{field}' est vide ou invalide.")
        
        # Validation optionnelle pour timeout et max_retries si présents
        if self.timeout is not None and self.timeout <= 0:
            raise ValueError("Le champ 'timeout' doit être un nombre positif.")
        if self.max_retries is not None and self.max_retries < 0:
            raise ValueError("Le champ 'max_retries' doit être un entier positif ou zéro.")
        