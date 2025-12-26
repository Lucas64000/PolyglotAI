"""
Configuration Base Module
"""
import os
from typing import Any
from pydantic import BaseModel, ConfigDict
from pydantic_core import CoreSchema, core_schema

class ImmutableConfig(BaseModel):
    """
    Configuration de base : Immuable et stricte.
    Empêche la modification accidentelle des configs au runtime.
    """
    model_config = ConfigDict(
        frozen=True,
        extra="ignore",
    )

def get_env(key: str, default: str | None = None) -> str:
    """
    Get environment variable with optional default.
    
    Args:
        key: Environment variable name
        default: Default value if not set
    
    Returns:
        Environment variable value or default
    """
    return os.environ.get(key, default) if default is not None else os.environ.get(key, "")


from dotenv import load_dotenv

load_dotenv()



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
    
    @classmethod
    def __get_pydantic_core_schema__(
        cls, source_type: Any, handler: Any
    ) -> CoreSchema:
        """
        Define how Pydantic should validate and serialize SecretString.
        
        This allows SecretString to be used as a field type in Pydantic models.
        """
        # Accept either a string (convert to SecretString) or an existing SecretString (pass through)
        return core_schema.union_schema([
            core_schema.is_instance_schema(cls),
            core_schema.no_info_after_validator_function(
                cls,
                core_schema.str_schema(),
            ),
        ], serialization=core_schema.plain_serializer_function_ser_schema(
            lambda x: "**********",
            info_arg=False,
        ))