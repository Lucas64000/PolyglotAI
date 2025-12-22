
from datetime import datetime
from src.application.ports import TimeProvider

class StubTimeProvider(TimeProvider):
    def __init__(self, now: datetime):
        self._now = now

    def now(self) -> datetime:
        return self._now
