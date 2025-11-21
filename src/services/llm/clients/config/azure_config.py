from dataclasses import dataclass
from typing import Any, Dict
from .config_interface import ClientConfig

from src.utils.logger import get_logger

logger = get_logger(__name__)

@dataclass(frozen=True)
class AzureClientConfig(ClientConfig):
    """Config du client Azure"""

    api_key: str
    azure_endpoint: str
    azure_deployment: str
    api_version: str
    
    timeout: float | None = None        
    max_retries: int | None = None     

    required_fields = ["api_key", "azure_endpoint", "azure_deployment", "api_version"]

    def __post_init__(self) -> None:
        self._validate(self.required_fields)

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
        