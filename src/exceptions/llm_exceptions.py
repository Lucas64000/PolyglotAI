"""Exceptions relatives aux LLM"""

class LLMError(Exception):
    """Erreur de base pour les LLM"""
    pass


class LLMResponseError(LLMError):
    """Réponse invalide du LLM"""
    pass


class LLMJSONDecodeError(LLMError):
    """Erreur de décodage JSON"""
    pass