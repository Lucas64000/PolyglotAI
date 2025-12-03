"""
Logging Configuration

Configuration for application logging.
"""

from typing import ClassVar, Literal, Self

from pydantic import Field, field_validator

from src.infrastructure.config.base import (
    ImmutableConfig,
    YAMLConfigLoader,
    get_env,
)


LogLevel = Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
LogFormat = Literal["json", "text"]


class LoggingConfig(ImmutableConfig, YAMLConfigLoader):
    """
    Application logging configuration.
    
    Environment variables:
    - LOG_LEVEL: Logging level (default: INFO)
    - LOG_FORMAT: Output format 'json' or 'text' (default: text)
    - LOG_FILE: Optional file path for log output
    
    YAML section: app.logging
    """
    
    yaml_section: ClassVar[tuple[str, ...]] = ("app", "logging")
    
    level: LogLevel = Field(
        default="INFO",
        description="Logging level",
    )
    format: LogFormat = Field(
        default="text",
        description="Log output format",
    )
    file: str | None = Field(
        default=None,
        description="Optional log file path",
    )
    
    @field_validator("level", mode="before")
    @classmethod
    def _normalize_level(cls, v: object) -> str:
        """Normalize log level to uppercase."""
        if isinstance(v, str):
            return v.upper()
        return str(v).upper()
    
    @classmethod
    def from_env(cls) -> Self:
        """
        Create logging config from environment variables.
        
        Loads defaults from YAML, then overrides with env vars.
        
        Returns:
            Validated logging configuration
        """
        yaml_defaults = cls._get_yaml_values()
        
        return cls(
            level=get_env("LOG_LEVEL", yaml_defaults.get("level", "INFO")) or "INFO",  # type: ignore[arg-type]
            format=get_env("LOG_FORMAT", yaml_defaults.get("format", "text")) or "text",  # type: ignore[arg-type]
            file=get_env("LOG_FILE", yaml_defaults.get("file")),
        )
