"""
RecordVocabulary Use Case

Handles storing new vocabulary items learned during conversation.
"""


from dataclasses import dataclass
from uuid import UUID

from src.core.ports.driven import GraphMemory, VocabularyRepository
from src.core.domain.entities import VocabularyItem
from src.core.domain.value_objects import Language, PartOfSpeech


@dataclass
class RecordVocabularyInput:
    """Input for recording vocabulary."""
    user_id: UUID
    term: str
    definition: str
    language: Language
    part_of_speech: PartOfSpeech | None = None
    context_example: str | None = None


@dataclass
class RecordVocabularyOutput:
    """Output from recording vocabulary."""
    vocabulary_item: VocabularyItem
    is_new: bool


class RecordVocabularyUseCase:
    """
    Use case for recording a vocabulary item.
    
    Handles the logic of:
    - Checking if the term already exists
    - Creating or updating the item
    - Storing in both repository and graph
    """
    
    def __init__(
        self,
        vocabulary_repository: VocabularyRepository,
        graph_memory: GraphMemory,
    ) -> None:
        self._vocab_repo = vocabulary_repository
        self._graph_memory = graph_memory
    
    async def execute(self, input_data: RecordVocabularyInput) -> RecordVocabularyOutput:
        """Execute the use case."""
        from src.core.domain.entities import VocabularyItem
        
        # Check if already exists
        existing = await self._vocab_repo.get_by_term(
            input_data.user_id,
            input_data.term,
            input_data.language,
        )
        
        if existing:
            return RecordVocabularyOutput(
                vocabulary_item=existing,
                is_new=False,
            )
        
        # Create new item
        item = VocabularyItem(
            term=input_data.term,
            definition=input_data.definition,
            language=input_data.language,
            part_of_speech=input_data.part_of_speech,
            context_example=input_data.context_example,
        )
        
        # Save to repository
        await self._vocab_repo.save(input_data.user_id, item)
        
        # Store in graph with relationships
        await self._graph_memory.store_vocabulary(input_data.user_id, item)
        
        return RecordVocabularyOutput(
            vocabulary_item=item,
            is_new=True,
        )
