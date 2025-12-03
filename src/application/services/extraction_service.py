"""
ExtractionService

Service for extracting vocabulary and errors from conversations
and storing them in the knowledge graph.

This is the glue between:
- LLM (for extraction via structured output)
- Domain entities (VocabularyItem, UserError)
- GraphMemory (for persistence)
"""

from uuid import UUID, uuid4
from typing import Any

from src.core.ports.driven import ChatModel, GraphMemory
from src.core.domain.entities import ChatMessage, VocabularyItem, UserError
from src.core.domain.value_objects import Language, ErrorType, PartOfSpeech, Role


# Prompt for structured extraction
EXTRACTION_PROMPT = """Analyze this conversation between a language tutor and a learner.
Extract:
1. New vocabulary words the learner should remember (only correct, dictionary-form words)
2. Mistakes the learner made (with corrections)

Respond in JSON format:
{
    "vocabulary": [
        {
            "term": "string (lemma/dictionary form)",
            "definition": "string (in learner's native language)",
            "pos": "NOUN|VERB|ADJ|ADV|null",
            "context_example": "string|null"
        }
    ],
    "errors": [
        {
            "wrong_form": "string (exact incorrect text)",
            "correction": "string (correct form)",
            "error_type": "GRAMMAR|SPELLING|VOCABULARY|PRONUNCIATION|CONJUGATION|SYNTAX",
            "explanation": "string (why it's wrong)"
        }
    ]
}

Only extract items that are pedagogically valuable. Skip trivial typos.
If nothing to extract, return empty arrays.
"""


class ExtractionService:
    """
    Service for extracting and persisting learning entities from conversations.
    
    Flow:
    1. Takes conversation messages
    2. Sends to LLM for structured extraction
    3. Converts LLM output to domain entities
    4. Stores in GraphMemory
    
    All dependencies are injected.
    """
    
    def __init__(
        self,
        chat_model: ChatModel,
        graph_memory: GraphMemory,
    ) -> None:
        """
        Initialize with injected dependencies.
        
        Args:
            chat_model: For LLM extraction
            graph_memory: For storing extracted entities
        """
        self._chat_model = chat_model
        self._graph_memory = graph_memory
    
    async def extract_and_store(
        self,
        user_id: UUID,
        conversation: list[ChatMessage],
        target_language: Language,
        native_language: Language,
    ) -> dict[str, Any]:
        """
        Extract vocabulary and errors from conversation and store in graph.
        
        Args:
            user_id: The learner's ID
            conversation: Recent conversation messages
            target_language: Language being learned
            native_language: Learner's native language
            
        Returns:
            Summary of what was extracted and stored
        """
        # 1. Build extraction prompt
        extraction_messages = self._build_extraction_messages(
            conversation, target_language, native_language
        )
        
        # 2. Call LLM for structured extraction
        extracted_data = await self._chat_model.generate_json(extraction_messages)
        
        # 3. Convert to domain entities and store
        stored_vocabulary = await self._process_vocabulary(
            user_id=user_id,
            raw_vocabulary=extracted_data.get("vocabulary", []),
            language=target_language,
        )
        
        stored_errors = await self._process_errors(
            user_id=user_id,
            raw_errors=extracted_data.get("errors", []),
            language=target_language,
        )
        
        return {
            "vocabulary_count": len(stored_vocabulary),
            "error_count": len(stored_errors),
            "vocabulary": [v.term for v in stored_vocabulary],
            "errors": [e.wrong_form for e in stored_errors],
        }
    
    def _build_extraction_messages(
        self,
        conversation: list[ChatMessage],
        target_language: Language,
        native_language: Language,
    ) -> list[ChatMessage]:
        """Build messages for extraction prompt."""
        # Format conversation for analysis
        conversation_text = "\n".join([
            f"{'Learner' if msg.role == Role.USER else 'Tutor'}: {msg.content}"
            for msg in conversation
        ])
        
        # Use session_id from conversation or generate a temporary one
        session_id = conversation[0].session_id if conversation else uuid4()
        
        system_message = ChatMessage(
            session_id=session_id,
            role=Role.SYSTEM,
            content=f"{EXTRACTION_PROMPT}\n\nTarget language: {target_language.name}\nNative language: {native_language.name}",
        )
        
        user_message = ChatMessage(
            session_id=session_id,
            role=Role.USER,
            content=f"Analyze this conversation:\n\n{conversation_text}",
        )
        
        return [system_message, user_message]
    
    async def _process_vocabulary(
        self,
        user_id: UUID,
        raw_vocabulary: list[dict[str, Any]],
        language: Language,
    ) -> list[VocabularyItem]:
        """Convert raw vocabulary data to entities and store."""
        stored: list[VocabularyItem] = []
        
        for raw in raw_vocabulary:
            try:
                # Parse part of speech if provided
                pos = None
                if raw.get("pos"):
                    try:
                        pos = PartOfSpeech(raw["pos"])
                    except ValueError:
                        pass
                
                # Create domain entity
                vocab_item = VocabularyItem(
                    term=raw["term"],
                    definition=raw["definition"],
                    language=language,
                    part_of_speech=pos,
                    context_example=raw.get("context_example"),
                )
                
                # Store in graph
                await self._graph_memory.store_vocabulary(user_id, vocab_item)
                stored.append(vocab_item)
                
            except (KeyError, ValueError):
                # Skip invalid items, log in production
                continue
        
        return stored
    
    async def _process_errors(
        self,
        user_id: UUID,
        raw_errors: list[dict[str, Any]],
        language: Language,
    ) -> list[UserError]:
        """Convert raw error data to entities and store."""
        stored: list[UserError] = []
        
        for raw in raw_errors:
            try:
                # Parse error type
                error_type = ErrorType.GRAMMAR  # default
                if raw.get("error_type"):
                    try:
                        error_type = ErrorType(raw["error_type"])
                    except ValueError:
                        pass
                
                # Create domain entity
                error = UserError(
                    user_id=user_id,
                    wrong_form=raw["wrong_form"],
                    correction=raw["correction"],
                    error_type=error_type,
                    language=language,
                    explanation=raw.get("explanation"),
                )
                
                # Store in graph (handles duplicates internally)
                await self._graph_memory.store_error(user_id, error)
                stored.append(error)
                
            except (KeyError, ValueError):
                # Skip invalid items
                continue
        
        return stored
