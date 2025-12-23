"""
Vocabulary Source Value Object

Represents where a learned vocabulary item originated in the learning context.
"""

from __future__ import annotations

from enum import Enum

class VocabularySource(Enum):
    """
    Source classification for vocabulary learning.
    
    Helps track where students encounter and produce vocabulary:
    - STUDENT: New words produced or used by the student in conversation
    - TEACHER: New words introduced by the teacher in explanations or responses
    
    This distinction is useful for adapting teaching strategy and understanding
    which words the student is actively producing versus passively receiving.
    """
    STUDENT = "student"
    TEACHER = "teacher"
