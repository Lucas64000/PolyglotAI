"""
Configuration Base Module

Provides the foundation for loading configuration from multiple sources:
1. YAML file (defaults and structure)
2. Environment variables (overrides and secrets)
"""

from abc import ABC, abstractmethod
from functools import lru_cache
from pathlib import Path
from typing import Any, ClassVar, Self

import yaml
import os
from pydantic import BaseModel, ConfigDict


def _get_project_root() -> Path:
    """Get project root directory (where config.yaml lives)."""
    current = Path(__file__).resolve()
    # Navigate up from src/infrastructure/config/base.py to project root
    return current.parent.parent.parent.parent


@lru_cache(maxsize=1)
def load_yaml_config() -> dict[str, Any]:
    """
    Load and cache the YAML configuration file.
    
    Returns:
        Parsed YAML configuration as a dictionary.
        Empty dict if file doesn't exist.
    
    Note:
        Cached to avoid re-reading the file on every config access.
    """
    config_path = _get_project_root() / "config.yaml"
    
    if not config_path.exists():
        return {}
    
    with config_path.open(encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


class ImmutableConfig(BaseModel):
    """
    Base class for immutable configuration objects.
    
    All config classes inherit from this to ensure:
    - Immutability (frozen)
    - No extra fields allowed
    - Validation on creation
    """
    
    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
        validate_default=True,
    )


class YAMLConfigLoader(ABC):
    """
    Mixin for loading configuration from YAML.
    
    Subclasses define their YAML path via `yaml_section` class variable.
    
    Example:
        class Neo4jConfig(ImmutableConfig, YAMLConfigLoader):
            yaml_section: ClassVar[tuple[str, ...]] = ("services", "neo4j")
    """
    
    yaml_section: ClassVar[tuple[str, ...]]
    
    @classmethod
    def _get_yaml_values(cls) -> dict[str, Any]:
        """
        Extract values from YAML config for this section.
        
        Returns:
            Dictionary of values from the YAML section.
            Empty dict if section doesn't exist.
        """
        result: dict[str, Any] | Any = load_yaml_config()
        
        for key in cls.yaml_section:
            if not isinstance(result, dict):
                return {}
            result = result.get(key, {})  # type: ignore[union-attr]
        
        if isinstance(result, dict):
            return dict(result)  # type: ignore[arg-type]
        return {}
    
    @classmethod
    @abstractmethod
    def from_env(cls) -> Self:
        """
        Create config from environment variables.
        
        This is the primary factory method. It should:
        1. Load YAML defaults
        2. Override with environment variables
        3. Validate the result
        
        Returns:
            Validated configuration instance.
        """
        ...


class SecretString:
    """
    A string that hides its value in repr/str for security.
    
    The actual value is accessible via `.get_secret_value()`.
    
    Example:
        api_key = SecretString("sk-xxx123")
        print(api_key)  # Output: SecretString('**********')
        print(api_key.get_secret_value())  # Output: sk-xxx123
    """
    
    __slots__ = ("_value",)
    
    def __init__(self, value: str) -> None:
        self._value = value
    
    def get_secret_value(self) -> str:
        """Get the actual secret value."""
        return self._value
    
    def __repr__(self) -> str:
        return "SecretString('**********')"
    
    def __str__(self) -> str:
        return "**********"
    
    def __eq__(self, other: object) -> bool:
        if isinstance(other, SecretString):
            return self._value == other._value
        return False
    
    def __hash__(self) -> int:
        return hash(self._value)
    
    def __bool__(self) -> bool:
        return bool(self._value)


def get_env(key: str, default: str | None = None) -> str | None:
    """
    Get environment variable with optional default.
    
    Args:
        key: Environment variable name
        default: Default value if not set
    
    Returns:
        Environment variable value or default
    """
    return os.environ.get(key, default)


def require_env(key: str) -> str:
    """
    Get required environment variable.
    
    Args:
        key: Environment variable name
    
    Returns:
        Environment variable value
    
    Raises:
        ConfigurationError: If the variable is not set
    """
    from src.core.exceptions import ConfigurationError
    
    value = os.environ.get(key)
    if value is None:
        raise ConfigurationError(
            f"Required environment variable '{key}' is not set",
            config_key=key
        )
    return value
