"""
Application Settings

Central aggregator for all configuration modules.

Architecture:
- Each config module handles its own domain (AI, database, logging)
- Settings aggregates them with lazy loading
- Use get_settings() at entrypoints only
- Inject specific configs via DI in services
"""

from functools import lru_cache

from src.infrastructure.config.base import (
    ImmutableConfig,
    YAMLConfigLoader,
    get_env,
    load_yaml_config,
)
from src.infrastructure.config.ai import AIProviderConfig
from src.infrastructure.config.database import Neo4jConfig
from src.infrastructure.config.logging import LoggingConfig


class AppConfig(ImmutableConfig, YAMLConfigLoader):
    """
    Core application configuration.
    
    Environment variables:
    - APP_NAME: Application name (default: PolyglotAI)
    - APP_DEBUG: Enable debug mode (default: false)
    
    YAML section: app
    """
    
    yaml_section = ("app",)
    
    name: str = "PolyglotAI"
    debug: bool = False
    
    @classmethod
    def from_env(cls) -> "AppConfig":
        """Create app config from environment variables."""
        yaml_defaults = cls._get_yaml_values()
        
        debug_str = get_env("APP_DEBUG", str(yaml_defaults.get("debug", "false"))) or "false"
        debug = debug_str.lower() in ("true", "1", "yes")
        
        return cls(
            name=get_env("APP_NAME", yaml_defaults.get("name", "PolyglotAI")) or "PolyglotAI",
            debug=debug,
        )


class Settings:
    """
    Main application settings - single entry point for all configuration.
    
    This class aggregates all configuration sections with lazy loading.
    Configurations are created on first access and cached.
    
    Usage:
        settings = get_settings()
        print(settings.app.name)
        print(settings.provider)  # e.g., "azure"
        print(settings.ai.get_chat_model())
    
    For dependency injection, prefer injecting specific configs:
        def __init__(self, neo4j_config: Neo4jConfig): ...
    
    Note:
        To get the factory (not just config), use AIProviderRegistry directly:
        
        from src.infrastructure.ai import AIProviderRegistry
        factory = AIProviderRegistry.create_factory(settings.provider)
    """
    
    __slots__ = (
        "_app",
        "_ai_provider",
        "_ai_config",
        "_neo4j",
        "_logging",
    )
    
    def __init__(self) -> None:
        """Initialize with empty cache."""
        self._app: AppConfig | None = None
        self._ai_provider: str | None = None
        self._ai_config: AIProviderConfig | None = None
        self._neo4j: Neo4jConfig | None = None
        self._logging: LoggingConfig | None = None
    
    @property
    def app(self) -> AppConfig:
        """Get application configuration."""
        if self._app is None:
            self._app = AppConfig.from_env()
        return self._app
    
    @property
    def provider(self) -> str:
        """
        Get the active AI provider name.
        
        This is determined by the AI_PROVIDER environment variable
        or the 'provider_llm_default' key in the YAML config.
        
        Returns:
            Provider name (e.g., "azure", "openai", "ollama")
        """
        if self._ai_provider is None:
            # Import here to avoid circular imports
            from src.infrastructure.ai.provider_registry import AIProviderRegistry
            
            yaml_config = load_yaml_config()
            general = yaml_config.get("general", {})
            default_provider = general.get("provider_llm_default", "azure")
            provider_str = get_env("AI_PROVIDER", default_provider) or "azure"
            
            # Validate provider is registered
            if not AIProviderRegistry.is_registered(provider_str):
                from src.core.exceptions import ConfigurationError
                available = ", ".join(AIProviderRegistry.list_providers())
                raise ConfigurationError(
                    f"Invalid AI_PROVIDER: '{provider_str}'. Available: {available}",
                    config_key="AI_PROVIDER"
                )
            
            self._ai_provider = provider_str
        
        return self._ai_provider
    
    @property
    def ai(self) -> AIProviderConfig:
        """
        Get AI provider configuration for the active provider.
        
        Uses AIProviderRegistry to dynamically resolve the config class
        based on the provider name. No hardcoded mapping needed.
        """
        if self._ai_config is None:
            # Import here to avoid circular imports
            from src.infrastructure.ai.provider_registry import AIProviderRegistry
            
            config_class = AIProviderRegistry.get_config_class(self.provider)
            self._ai_config = config_class.from_env()
        
        assert self._ai_config is not None  # Guaranteed by lazy loading above
        return self._ai_config
    
    @property
    def neo4j(self) -> Neo4jConfig:
        """Get Neo4j database configuration."""
        if self._neo4j is None:
            self._neo4j = Neo4jConfig.from_env()
        return self._neo4j
    
    @property
    def logging(self) -> LoggingConfig:
        """Get logging configuration."""
        if self._logging is None:
            self._logging = LoggingConfig.from_env()
        return self._logging
    
    def __repr__(self) -> str:
        return f"Settings(provider={self.provider!r})"


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """
    Get cached settings instance.
    
    Settings are loaded once and cached for the application lifetime.
    Call this function instead of instantiating Settings directly.
    
    Note:
        This is intended for use at entrypoints only (main, CLI, API routes).
        Services should receive their configuration via dependency injection,
        NOT by calling this function directly.
    
    Returns:
        Cached Settings instance
    
    Example:
        settings = get_settings()
        if settings.app.debug:
            print(f"Running {settings.app.name} in debug mode")
        
        # Access AI config
        ai_config = settings.ai
        print(f"Using {ai_config.chat_model}")
    """
    return Settings()
