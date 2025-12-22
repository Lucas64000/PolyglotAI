"""
System Time Provider Adapter

Real implementation of TimeProvider using the system clock.
"""

from datetime import datetime, timezone


class SystemTimeProvider:
    """
    Implementation of TimeProvider that uses the actual system time.
    """

    def get_current_time(self) -> datetime:
        """Return the current system time in UTC."""
        return datetime.now(timezone.utc)