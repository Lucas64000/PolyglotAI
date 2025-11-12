"""
Config Loader - Version POC Simple
Juste charger .env + yaml, pas de patterns complexes
"""

from pathlib import Path
from typing import Optional
import os
import yaml
from dotenv import load_dotenv


class Config:
    """
    Configuration simple pour POC
    
    Charge .env et config.yaml
    Pas de patterns complexes, juste ce qui marche
    """
    
    def __init__(self):
        # Charge .env
        load_dotenv()
        
        # Charge yaml
        config_path = Path("config/config.yaml")
        with open(config_path) as f:
            self.yaml = yaml.safe_load(f)

        self.azure_api_key = os.getenv("AZURE_API_KEY")
        self.api_version = os.getenv("API_VERSION")
        self.azure_endpoint = os.getenv("AZURE_ENDPOINT")
        self.model_id = os.getenv("MODEL_ID")
        self.debug = os.getenv("DEBUG", "true").lower() == "true"
    
    @property
    def llm_model(self) -> str:
        """Modèle LLM à utiliser"""
        return self.yaml["llm"]["model"]
    
    @property
    def llm_temperature(self) -> float:
        """Température LLM"""
        return self.yaml["llm"]["temperature"]
    
    @property
    def llm_max_tokens(self) -> int:
        """Max tokens LLM"""
        return self.yaml["llm"]["max_tokens"]
    
    @property
    def memory_window_size(self) -> int:
        """Taille fenêtre mémoire"""
        return self.yaml["memory"]["window_size"]
    
    @property
    def memory_summary_frequency(self) -> int:
        """Fréquence résumé"""
        return self.yaml["memory"]["summary_frequency"]
    
    @property
    def evaluation_frequency(self) -> int:
        """Fréquence évaluation"""
        return self.yaml["evaluation"]["frequency"]


# Singleton global (simple pour POC)
_config: Optional[Config] = None

def get_config() -> Config:
    """Récupère la config (singleton)"""
    global _config
    if _config is None:
        _config = Config()
    return _config