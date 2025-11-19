"""
Fonctions utils générales
"""

from datetime import datetime, timezone


def utc_now() -> datetime:
    """Retourne la date/heure UTC actuelle."""
    return datetime.now(timezone.utc)