"""
Chat DTOs

Data transfer objects for chat/conversation operations.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any
from uuid import UUID


@dataclass
class ChatRequest:
    """Request to send a chat message."""
    session_id: UUID
    message: str
    metadata: dict[str, Any] = field(default_factory=dict[str, Any])


@dataclass
class ChatResponse:
    """Response from the chat service."""
    session_id: UUID
    message_id: UUID
    content: str
    timestamp: datetime
    metadata: dict[str, Any] = field(default_factory=dict[str, Any])


@dataclass
class SessionInfo:
    """Information about a learning session."""
    session_id: UUID
    user_id: UUID
    started_at: datetime
    ended_at: datetime | None = None
    focus_topic: str | None = None
    message_count: int = 0
    duration_minutes: float = 0.0
    is_active: bool = True
