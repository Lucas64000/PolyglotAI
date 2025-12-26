"""
Ollama Configuration

Configuration for the Ollama local LLM provider.
"""

from typing import Self
from pydantic import Field, field_validator
from .base import ImmutableConfig, get_env


class OllamaConfig(ImmutableConfig):
    """
    Ollama local LLM configuration.
    
    Env variables:
    - OLLAMA_BASE_URL: Ollama server URL (default: http://localhost:11434)
    - OLLAMA_CHAT_MODEL: Chat model (default: qwen2.5:7b)
    
    Note:
        Ollama runs locally so no API key is required.
        Ensure Ollama is running and the models are pulled before use.
    """
    base_url: str = Field(default="http://localhost:11434")
    model: str = Field(default="qwen2.5:7b")
    temperature: float = Field(default=0.7)
    
    def model_name(self) -> str:
        """Get the chat model name."""
        return self.model
    
    @field_validator("base_url")
    @classmethod
    def _validate_base_url(cls, v: str) -> str:
        """Ensure base_url is a valid HTTP(S) URL."""
        if not v.startswith(("http://", "https://")):
            raise ValueError("Ollama base URL must be an HTTP or HTTPS URL")
        return v.rstrip("/")
    
    @property
    def openai_compatible_url(self) -> str:
        """Get the OpenAI-compatible API endpoint."""
        return f"{self.base_url}/v1"
    
    @classmethod
    def from_env(cls) -> Self:
        """
        Create Ollama config from environment variables.
        
        Returns:
            Validated Ollama configuration
        """
        return cls(
            base_url=get_env("OLLAMA_BASE_URL", "http://localhost:11434"),
            model=get_env("OLLAMA_MODEL", "qwen2.5:7b"),
            temperature=float(get_env("LLM_TEMPERATURE", "0.7")),
        )
