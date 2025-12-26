"""
Application Settings

Central aggregator for all configuration modules.
"""

from functools import lru_cache
from .ollama import OllamaConfig

class Settings:
    """
    This class aggregates all configuration sections with lazy loading.
    Configurations are created on first access and cached.
    """
    def __init__(self):
        self._ollama: OllamaConfig | None = None

    @property
    def ollama(self) -> OllamaConfig:
        if self._ollama is None:
            self._ollama = OllamaConfig.from_env()
        return self._ollama

@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """
    Get cached settings instance.
    
    Settings are loaded once and cached for the application lifetime.
    Call this function instead of instantiating Settings directly.
    
    Returns:
        Cached Settings instance
    """
    return Settings()
