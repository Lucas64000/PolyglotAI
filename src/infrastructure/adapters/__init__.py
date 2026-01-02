"""
Adapters Package

Adapters that connect the application to external systems.

Structure:
- driving/ : Primary/inbound adapters (receive requests from outside)
  - fastapi/ : HTTP REST API
"""

from .driven import LLMTeacherAdapter

__all__ = [
    "LLMTeacherAdapter",
]