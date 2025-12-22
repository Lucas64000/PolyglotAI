"""
Base Exception Classes

Defines the exception hierarchy for the domain layer.
"""


class DomainException(Exception):
    """
    Base exception for all domain-level errors.
    
    Domain exceptions represent violations of business rules and invariants.
    All domain-specific exceptions should inherit from this class.
    """
    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(self.message)