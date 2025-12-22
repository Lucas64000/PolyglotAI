"""
Time Provider Port

Interface for retrieving the current time.
"""

from typing import Protocol
from datetime import datetime


class TimeProvider(Protocol):
    """
    Port for time-related operations.
    """
    
    def now(self) -> datetime:
        """
        Get the current date and time (UTC).
        """
        ...