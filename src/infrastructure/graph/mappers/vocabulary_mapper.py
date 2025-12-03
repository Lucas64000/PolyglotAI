"""
Vocabulary Mapper

Converts between VocabularyItem entities and graph nodes.
"""

from typing import Any

from src.core.domain.entities import VocabularyItem
from src.infrastructure.graph.ontology import Vocabulary, Definition


class VocabularyMapper:
    """
    Maps between VocabularyItem domain entity and graph nodes.
    
    A VocabularyItem maps to:
    - One Vocabulary node (the term)
    - One Definition node (the meaning)
    - One HasDefinition edge connecting them
    """
    
    @staticmethod
    def to_graph_nodes(item: VocabularyItem) -> tuple[Vocabulary, Definition]:
        """
        Convert VocabularyItem to graph node objects.
        
        Returns:
            Tuple of (Vocabulary, Definition) Pydantic models
        """
        vocab_node = Vocabulary(
            term=item.term,
            language=item.language.code,
            pos=item.part_of_speech.value if item.part_of_speech else None,
        )
        
        definition_node = Definition(
            text=item.definition,
            context_usage=item.context_usage,
        )
        
        return vocab_node, definition_node
    
    @staticmethod
    def to_edge_data(item: VocabularyItem) -> dict[str, Any]:
        """
        Convert VocabularyItem to MemoryTrace edge data.
        
        Returns:
            Dictionary of edge properties for SRS tracking
        """
        return {
            "stability": item.stability,
            "last_review": item.last_reviewed.isoformat() if item.last_reviewed else None,
            "review_count": item.review_count,
        }
    
    @staticmethod
    def from_graph_nodes(
        vocab_data: dict[str, Any],
        definition_data: dict[str, Any],
        memory_trace_data: dict[str, Any] | None = None,
    ) -> VocabularyItem:
        """
        Convert graph node data to VocabularyItem.
        
        Args:
            vocab_data: Vocabulary node properties
            definition_data: Definition node properties
            memory_trace_data: Optional MemoryTrace edge properties
            
        Returns:
            VocabularyItem entity
        """
        from src.core.domain.entities import VocabularyItem
        from src.core.domain.value_objects import Language, PartOfSpeech
        
        stability = 0.1
        last_reviewed = None
        
        if memory_trace_data:
            stability = memory_trace_data.get("stability", 0.1)
            last_reviewed = memory_trace_data.get("last_review")
        
        pos = None
        if vocab_data.get("pos"):
            try:
                pos = PartOfSpeech(vocab_data["pos"])
            except ValueError:
                pass
        
        return VocabularyItem(
            term=vocab_data["term"],
            definition=definition_data["text"],
            language=Language(vocab_data["language"]),
            part_of_speech=pos,
            context_usage=definition_data.get("context_usage"),
            stability=stability,
            last_reviewed=last_reviewed,
        )
