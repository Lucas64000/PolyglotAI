# enums

from enum import Enum

class CECRLevel(str, Enum):
    A1 = "A1"
    A2 = "A2"
    B1 = "B1"
    B2 = "B2"
    C1 = "C1"
    C2 = "C2"

    @property
    def numeric_value(self) -> int:
        return list(CECRLevel).index(self) + 1 


class Language(str, Enum):
    FRENCH = "french"
    ENGLISH = "english"


class Role(str, Enum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


class ConversationStatus(str, Enum):
    ACTIVE = "active"
    ARCHIVED = "archived"
    DELETED = "deleted"


class Intent(str, Enum):
    EXERCISE = "exercise"
    TUTOR = "tutor"