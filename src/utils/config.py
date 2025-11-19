"""
Config Loader 
"""

import os
import yaml
import threading
from pathlib import Path
from typing import Dict, Any, List
from dotenv import load_dotenv

from src.utils.logger import get_logger

logger = get_logger(__name__)
CONFIG_PATH = Path("config.yaml") 

class Config:
    """
    Configuration centralisée de l'application
    
    Gère :
    - Variables d'environnement (.env) pour les secrets
    - Fichier YAML (config.yaml) pour les paramètres
    - Validation stricte au démarrage via Pydantic
    """
    
    def __init__(self):
        load_dotenv()
        
        if not CONFIG_PATH.exists():
            raise FileNotFoundError(
                f"Fichier de configuration non trouvé : {CONFIG_PATH}"
            )
        
        try:
            with open(CONFIG_PATH) as f:
                yaml_data: Dict[str, Any] = yaml.safe_load(f)
        except yaml.YAMLError as e:
            raise ValueError(f"Erreur de parsing YAML : {e}")
        
        self.general_config = yaml_data.get("general", {})
        self.services_config = yaml_data.get("services", {})
        self.providers_config = self.services_config.get("providers", {})
        self.llm_config = yaml_data.get("llm", {})

        self.provider_default = self.general_config.get("provider_llm_default", "")
        self.model_name_default = self.get_provider_config(self.provider_default).get("model_name_default", "")
        
        self.temperature_default = float(self.llm_config.get("temperature_default", 0.7))
        self.max_tokens_default = int(self.llm_config.get("max_tokens_default", 1000))
        self.context_history_length_default = int(self.llm_config.get("context_history_length_default", 5))


    def get_provider_config(self, provider_name: str) -> Dict[str, Any]:
        """
        Récupère la configuration d'un provider
        
        Args:
            provider_name: Nom du provider
            
        Returns:
            Configuration du provider
        """
        return self.providers_config.get(provider_name, {})

    def get_available_providers(self) -> List[str]:
        """
        Récupère la liste des providers disponibles
        
        Returns:
            Liste des noms de providers
        """
        return list(self.providers_config.keys())

    def get_env(self, key: str) -> str:
        """
        Récupère une variable d'environnement
        
        Args:
            key: Nom de la variable d'environnement
            
        Returns:
            La valeur de la variable 
        """
        value = os.getenv(key)
        
        if not value:
            logger.error(f"Variable d'environnement manquante : {key}")
            raise ValueError(
                f"Variable {key} manquante.\n"
                f"Ajoutez {key}=votre_clé dans le fichier .env"
            )
        
        return value

# =======================================================================
# Singleton 
# =======================================================================

_config: Config | None = None
_config_lock = threading.Lock()

def get_config() -> Config:
    """
    Récupère la configuration 
    
    Returns:
        Instance unique de Config
    """
    global _config
    
    if _config is None:
        with _config_lock:
            if _config is None:
                _config = Config()
    
    return _config