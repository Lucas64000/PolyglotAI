from dataclasses import dataclass
from typing import Any, Dict
from .config_interface import ClientConfig

from src.utils.logger import get_logger

logger = get_logger(__name__)

@dataclass(frozen=True)
class OllamaClientConfig(ClientConfig):
    base_url: str
    timeout: float | None = None        
    max_retries: int | None = None     
    
    required_fields = ["base_url"]
    
    def __post_init__(self) -> None:
        self._validate(self.required_fields)
    
    def to_sdk_kwargs(self) -> Dict[str, Any]:
        kwargs: Dict[str, Any] = {
            "base_url": self.base_url,
            "api_key": "ollama"
        }
        if self.timeout is not None:
            kwargs["timeout"] = self.timeout
        if self.max_retries is not None:
            kwargs["max_retries"] = self.max_retries
        return kwargs
        