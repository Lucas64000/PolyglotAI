"""
Vocabulary Source Value Object

Represents where a learned vocabulary item originated in the learning context.
"""

from __future__ import annotations

from enum import Enum

class VocabularySource(str, Enum):
    """
    Source classification for vocabulary learning.
    
    Helps track where learners encounter and produce vocabulary:
    - LEARNER: New words produced or used by the learner in conversation
    - TUTOR: New words introduced by the AI tutor in explanations or responses
    
    This distinction is useful for adapting teaching strategy and understanding
    which words the learner is actively producing versus passively receiving.
    """
    LEARNER = "learner"
    TUTOR = "tutor"
