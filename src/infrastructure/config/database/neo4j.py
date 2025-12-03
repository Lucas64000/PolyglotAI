"""
Neo4j Database Configuration

Configuration for Neo4j graph database connection.
"""

from typing import ClassVar, Self

from pydantic import Field, field_validator

from src.core.exceptions import ConfigurationError
from src.infrastructure.config.base import (
    ImmutableConfig,
    SecretString,
    YAMLConfigLoader,
    get_env,
    require_env,
)


class Neo4jConfig(ImmutableConfig, YAMLConfigLoader):
    """
    Neo4j database connection configuration.
    
    Environment variables:
    - NEO4J_URI: Connection URI (default: bolt://localhost:7687)
    - NEO4J_USER: Username (default: neo4j)
    - NEO4J_PASSWORD: Password (required)
    - NEO4J_DATABASE: Database name (default: neo4j)
    - NEO4J_POOL_SIZE: Connection pool size (default: 50)
    - NEO4J_CONNECTION_TIMEOUT: Connection timeout in seconds (default: 30)
    
    YAML section: services.neo4j
    """
    
    yaml_section: ClassVar[tuple[str, ...]] = ("services", "neo4j")
    
    uri: str = Field(
        default="bolt://localhost:7687",
        description="Neo4j connection URI",
    )
    user: str = Field(
        default="neo4j",
        description="Neo4j username",
    )
    password: SecretString = Field(
        description="Neo4j password",
    )
    database: str = Field(
        default="neo4j",
        description="Neo4j database name",
    )
    pool_size: int = Field(
        default=50,
        ge=1,
        le=1000,
        description="Connection pool size",
    )
    connection_timeout: int = Field(
        default=30,
        ge=1,
        le=300,
        description="Connection timeout in seconds",
    )
    
    @field_validator("uri")
    @classmethod
    def _validate_uri(cls, v: str) -> str:
        """Validate Neo4j URI format."""
        valid_schemes = ("bolt://", "bolt+s://", "neo4j://", "neo4j+s://")
        if not v.startswith(valid_schemes):
            raise ConfigurationError(
                f"Neo4j URI must start with one of: {', '.join(valid_schemes)}",
                config_key="NEO4J_URI"
            )
        return v
    
    @classmethod
    def from_env(cls) -> Self:
        """
        Create Neo4j config from environment variables.
        
        Loads defaults from YAML, then overrides with env vars.
        
        Returns:
            Validated Neo4j configuration
        """
        yaml_defaults = cls._get_yaml_values()
        
        return cls(
            uri=get_env("NEO4J_URI", yaml_defaults.get("uri", "bolt://localhost:7687")) or "bolt://localhost:7687",
            user=get_env("NEO4J_USER", yaml_defaults.get("user", "neo4j")) or "neo4j",
            password=SecretString(require_env("NEO4J_PASSWORD")),
            database=get_env("NEO4J_DATABASE", yaml_defaults.get("database", "neo4j")) or "neo4j",
            pool_size=int(get_env("NEO4J_POOL_SIZE", str(yaml_defaults.get("pool_size", 50))) or 50),
            connection_timeout=int(get_env("NEO4J_CONNECTION_TIMEOUT", str(yaml_defaults.get("connection_timeout", 30))) or 30),
        )
