"""
Use Cases Package

Application services that orchestrate business operations.
Each use case represents a single user action or system operation.
"""

from .send_message import SendMessageUseCase

__all__ = [
    "SendMessageUseCase",
]