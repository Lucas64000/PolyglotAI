"""
Base Exception Classes

Defines the exception hierarchy for the application.
"""

class PolyglotException(Exception):
    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(self.message)


class DomainException(PolyglotException):
    """
    Base exception for all domain-level errors.
    
    Domain exceptions represent violations of business rules and invariants.
    All domain-specific exceptions should inherit from this class.
    """


class InfrastructureError(PolyglotException):
    """
    Base class for exceptions originating from infrastructure layers.
    Indicates a failure in an external system or service.
    """