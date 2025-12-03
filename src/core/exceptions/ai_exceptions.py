"""
AI Exceptions

Exceptions for AI/LLM related errors.
These are infrastructure-level exceptions for external service failures.
"""

from .domain_exceptions import DomainException


class LLMError(DomainException):
    """
    Raised when an LLM API call fails.
    
    Examples:
        - Network timeout
        - Authentication failure
        - Rate limiting
        - Service unavailable
    """
    
    def __init__(self, provider: str, message: str, original_error: Exception | None = None) -> None:
        self.provider = provider
        self.original_error = original_error
        super().__init__(f"LLM error with {provider}: {message}")


class LLMResponseError(DomainException):
    """
    Raised when an LLM returns an invalid or empty response.
    
    Examples:
        - Empty response
        - Malformed response structure
        - Unexpected response format
    """
    
    def __init__(self, provider: str, message: str) -> None:
        self.provider = provider
        super().__init__(f"LLM response error with {provider}: {message}")


class LLMJSONDecodeError(DomainException):
    """
    Raised when an LLM response cannot be parsed as valid JSON.
    
    Examples:
        - Invalid JSON syntax
        - Unexpected JSON structure
    """
    
    def __init__(self, provider: str, message: str, raw_response: str) -> None:
        self.provider = provider
        self.raw_response = raw_response
        super().__init__(f"LLM JSON decode error with {provider}: {message}")


class EmbeddingError(DomainException):
    """
    Raised when an embedding API call fails.
    
    Examples:
        - Network timeout
        - Authentication failure
        - Rate limiting
        - Service unavailable
    """
    
    def __init__(self, provider: str, message: str, original_error: Exception | None = None) -> None:
        self.provider = provider
        self.original_error = original_error
        super().__init__(f"Embedding error with {provider}: {message}")


class EmbeddingResponseError(DomainException):
    """
    Raised when an embedding returns an invalid or empty response.
    
    Examples:
        - Empty response
        - Malformed response structure
        - Unexpected response format
    """
    
    def __init__(self, provider: str, message: str) -> None:
        self.provider = provider
        super().__init__(f"Embedding response error with {provider}: {message}")