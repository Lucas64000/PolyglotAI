"""
Config Loader 
"""

import os
import yaml
import threading
from pathlib import Path
from typing import Dict, Any
from dotenv import load_dotenv

from src.utils.logger import get_logger
from src.models.config_model import AppConfig, ProviderConfig

logger = get_logger(__name__)
CONFIG_PATH = Path("config/config.yaml") 

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
        
        # Vérification de la config
        try:
            general_config = yaml_data.get("general", {})
            self._app_config = AppConfig(
                active_llm_provider=general_config.get("active_llm_provider", "azure"),
                providers={
                    provider_name: ProviderConfig(**provider_data)
                    for provider_name, provider_data in yaml_data.get("providers", {}).items()
                }
            )
        except Exception as e:
            raise ValueError(f"Erreur de validation de la config : {e}")
        
        self._yaml = yaml_data
        
        # Chargement des secrets
        self._azure_api_key = self._get_env("AZURE_API_KEY")
        self._mistral_api_key = self._get_env("MISTRAL_API_KEY")

        self._azure_endpoint = self._get_env("AZURE_ENDPOINT")
        self._mistral_endpoint = self._get_env("MISTRAL_ENDPOINT")
        
        self._validate_provider_secrets()
        
        logger.info("Configuration chargée et validée avec succès")
        logger.info(f"Provider actif : {self.active_llm_provider}")

    # =======================================================================
    # Fonctions privées
    # =======================================================================
    
    def _get_env(self, key: str) -> str:
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
        
        if value:
            logger.debug(f"Variable {key} chargée avec succès")
        
        return value
    
    def _validate_provider_secrets(self):
        """
        Valide que les secrets du provider actif sont présents
        """
        provider = self.active_llm_provider
        
        if provider == "azure":
            if not self._azure_api_key:
                raise ValueError(
                    "AZURE_API_KEY manquante dans .env mais provider 'azure' est actif"
                )
            if not self._azure_endpoint:
                raise ValueError(
                    "AZURE_ENDPOINT manquant dans .env mais provider 'azure' est actif"
                )
        
        # Logique à revoir lors de l'implémentation du provider Mistral
        elif provider == "mistral":
            if not self._mistral_api_key:
                raise ValueError(
                    "MISTRAL_API_KEY manquante dans .env mais provider 'mistral' est actif"
                )
            if not self._mistral_endpoint:
                raise ValueError(
                    "MISTRAL_ENDPOINT manquant dans .env mais provider 'mistral' est actif"
                )
        
        logger.info(f"Secrets du provider '{provider}' validés")

    # =======================================================================
    # Propriétés de Sélection 
    # =======================================================================
    
    @property
    def active_llm_provider(self) -> str:
        """Détermine le fournisseur LLM actif basé sur le YAML"""
        provider = self._app_config.active_llm_provider.lower()
        
        supported = ["azure", "mistral"]
        if provider not in supported:
            raise ValueError(
                f"Provider '{provider}' invalide.\n"
                f"Providers supportés : {', '.join(supported)}"
            )
        
        return provider 

    def get_provider_config(self) -> ProviderConfig:
        """Récupère la configuration spécifique du provider actif"""
        provider = self.active_llm_provider
        
        if provider not in self._app_config.providers:
            raise ValueError(
                f"Configuration du provider '{provider}' manquante dans config.yaml"
            )
        
        return self._app_config.providers[provider]

    # =======================================================================
    # Propriétés des Secrets
    # =======================================================================

    @property
    def azure_api_key(self) -> str:
        """Clé API Azure"""
        return self._azure_api_key
    
    @property
    def mistral_api_key(self) -> str:
        """Clé API Mistral"""
        return self._mistral_api_key

    @property
    def azure_endpoint(self) -> str:
        """Endpoint Azure"""
        return self._azure_endpoint
    
    @property
    def mistral_endpoint(self) -> str:
        """Endpoint Mistral"""
        return self._mistral_endpoint

    # =======================================================================
    # Propriétés Dynamiques (basées sur le provider actif)
    # =======================================================================

    @property
    def llm_api_version(self) -> str:
        """Version API du provider actif"""
        provider_config = self.get_provider_config()
        return provider_config.api_version

    @property
    def llm_router(self) -> str:
        """Modèle/Déploiement pour le Router Agent"""
        provider_config = self.get_provider_config()
        return provider_config.deployment_name_router

    @property
    def llm_agent(self) -> str:
        """Modèle/Déploiement par défaut pour les agents"""
        provider_config = self.get_provider_config()
        return provider_config.deployment_name_default
        
    # =======================================================================
    # Propriétés Générales
    # =======================================================================
    
    @property
    def llm_temperature(self) -> float:
        """Température LLM par défaut"""
        return float(self._yaml["llm"]["temperature_default"])
    
    @property
    def llm_max_tokens(self) -> int:
        """Max tokens LLM"""
        return int(self._yaml["llm"]["max_tokens_default"])
        
    @property
    def context_history_length(self) -> int:
        """Nombre de messages servant de contexte au LLM"""
        return int(self._yaml["llm"]["context_history_length_default"])
    
    # =======================================================================
    # Représentation (safe pour les logs)
    # =======================================================================
    
    def __repr__(self) -> str:
        """Représentation sûre pour les logs"""
        return (
            f"Config("
            f"provider={self.active_llm_provider}, "
            f"router={self.llm_router}, "
            f"default={self.llm_agent}, "
            f"max_tokens={self.llm_max_tokens}, "
            f"temperature={self.llm_temperature}, "
            f")"
        )


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