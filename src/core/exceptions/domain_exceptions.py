"""
Domain Exceptions

All domain-level exceptions inherit from DomainException.
These represent business rule violations, not technical errors.
"""


class DomainException(Exception):
    """
    Base exception for all domain errors.
    
    Domain exceptions represent violations of business rules.
    """
    
    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(self.message)


class ValidationError(DomainException):
    """
    Raised when domain validation fails.
    
    Examples:
        - Empty required field
        - Invalid value range
        - Format violations
    """
    
    def __init__(self, field: str, message: str) -> None:
        self.field = field
        super().__init__(f"Validation error on '{field}': {message}")


class EntityNotFoundError(DomainException):
    """
    Raised when a requested entity does not exist.
    
    Examples:
        - User not found
        - Vocabulary item not found
        - Session not found
    """
    
    def __init__(self, entity_type: str, entity_id: str) -> None:
        self.entity_type = entity_type
        self.entity_id = entity_id
        super().__init__(f"{entity_type} with id '{entity_id}' not found")


class InvalidLanguagePairError(DomainException):
    """
    Raised when an invalid language pair is specified.
    
    Examples:
        - Source and target are the same
        - Unsupported language code
    """
    
    def __init__(self, source: str, target: str, reason: str) -> None:
        self.source = source
        self.target = target
        super().__init__(f"Invalid language pair '{source}' -> '{target}': {reason}")


class InvalidCEFRLevelError(DomainException):
    """
    Raised when an invalid CEFR level is specified.
    """
    
    def __init__(self, level: str) -> None:
        self.level = level
        super().__init__(f"Invalid CEFR level: '{level}'. Valid levels: A1, A2, B1, B2, C1, C2")


class SessionNotActiveError(DomainException):
    """
    Raised when trying to perform an operation on an inactive session.
    
    Examples:
        - Adding a message to an ended session
        - Ending an already ended session
    """
    
    def __init__(self, session_id: str) -> None:
        self.session_id = session_id
        super().__init__(f"Session '{session_id}' is not active")


class ConfigurationError(DomainException):
    """
    Raised when there is a configuration issue.
    
    Examples:
        - Invalid provider configuration
        - Missing required settings
        - Unsupported model or deployment
    """
    
    def __init__(self, message: str, config_key: str | None = None) -> None:
        self.config_key = config_key
        super().__init__(f"Configuration error: {message}")
