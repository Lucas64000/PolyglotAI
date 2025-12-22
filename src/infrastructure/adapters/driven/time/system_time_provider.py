"""
System Time Provider Adapter

Real implementation of TimeProvider using the system clock.
"""

from datetime import datetime, timezone
from src.core.ports import TimeProvider


class SystemTimeProvider(TimeProvider):
    """
    Implementation of TimeProvider that uses the actual system time.
    """

    def now(self) -> datetime:
        """Return the current system time in UTC."""
        return datetime.now(timezone.utc)