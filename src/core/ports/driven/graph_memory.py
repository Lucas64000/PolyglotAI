"""
GraphMemory Port

Interface for the knowledge graph memory system.
Abstracts away Graphiti/Neo4j implementation details.
"""

from abc import abstractmethod
from typing import Any, Protocol
from uuid import UUID

from ...domain.entities import (
    GrammarRule,
    UserError,
    VocabularyItem,
)


class GraphMemory(Protocol):
    """
    Interface for the knowledge graph memory system.
    
    This Protocol abstracts the graph database operations,
    allowing the application to store and retrieve learning data.
    
    Usage:
        ```python
        # Store a vocabulary item
        await graph_memory.store_vocabulary(user_id, vocab_item)
        
        # Retrieve relevant context for the conversation
        context = await graph_memory.get_learning_context(
            user_id, 
            current_topic="past tense verbs"
        )
        ```
    """
    
    # ==========================================
    # Vocabulary Operations
    # ==========================================
    
    @abstractmethod
    async def store_vocabulary(
        self,
        user_id: UUID,
        vocabulary: VocabularyItem,
    ) -> None:
        """
        Store a vocabulary item in the user's knowledge graph.
        
        Creates:
        - Vocabulary node
        - Definition node
        - MemoryTrace edge (User -> Vocabulary)
        
        Args:
            user_id: The user's unique identifier
            vocabulary: The vocabulary item to store
        """
        ...
    
    @abstractmethod
    async def get_vocabulary(
        self,
        user_id: UUID,
        term: str,
    ) -> VocabularyItem | None:
        """
        Retrieve a vocabulary item by term.
        
        Args:
            user_id: The user's unique identifier
            term: The term to look up
            
        Returns:
            VocabularyItem if found, None otherwise
        """
        ...
    
    @abstractmethod
    async def get_vocabulary_for_review(
        self,
        user_id: UUID,
        limit: int = 10,
    ) -> list[VocabularyItem]:
        """
        Get vocabulary items that need review.
        
        Based on SRS algorithm, returns items with low stability
        or that haven't been reviewed recently.
        
        Args:
            user_id: The user's unique identifier
            limit: Maximum number of items to return
            
        Returns:
            List of vocabulary items needing review
        """
        ...
    
    @abstractmethod
    async def update_vocabulary_mastery(
        self,
        user_id: UUID,
        term: str,
        correct: bool,
    ) -> None:
        """
        Update mastery level after a review.
        
        Args:
            user_id: The user's unique identifier
            term: The term that was reviewed
            correct: Whether the user recalled it correctly
        """
        ...
    
    # ==========================================
    # Error Tracking Operations
    # ==========================================
    
    @abstractmethod
    async def store_error(
        self,
        user_id: UUID,
        error: UserError,
    ) -> None:
        """
        Store a user error in the knowledge graph.
        
        Creates:
        - Mistake node
        - StrugglesWith edge (User -> Mistake)
        - Optional: BelongsTo edge (Mistake -> GrammarRule)
        
        Args:
            user_id: The user's unique identifier
            error: The error to store
        """
        ...
    
    @abstractmethod
    async def get_recurring_errors(
        self,
        user_id: UUID,
        limit: int = 5,
    ) -> list[UserError]:
        """
        Get the user's most common errors.
        
        Args:
            user_id: The user's unique identifier
            limit: Maximum number of errors to return
            
        Returns:
            List of recurring errors, sorted by frequency
        """
        ...
    
    @abstractmethod
    async def increment_error_count(
        self,
        user_id: UUID,
        wrong_form: str,
    ) -> None:
        """
        Increment the occurrence count for an existing error.
        
        Args:
            user_id: The user's unique identifier
            wrong_form: The incorrect form to look up
        """
        ...
    
    # ==========================================
    # Grammar Rule Operations
    # ==========================================
    
    @abstractmethod
    async def store_grammar_rule(
        self,
        rule: GrammarRule,
    ) -> None:
        """
        Store a grammar rule in the knowledge graph.
        
        Args:
            rule: The grammar rule to store
        """
        ...
    
    @abstractmethod
    async def get_grammar_rule(
        self,
        rule_name: str,
    ) -> GrammarRule | None:
        """
        Retrieve a grammar rule by name.
        
        Args:
            rule_name: The name of the rule
            
        Returns:
            GrammarRule if found, None otherwise
        """
        ...
    
    # ==========================================
    # Context & Search Operations
    # ==========================================
    
    @abstractmethod
    async def get_learning_context(
        self,
        user_id: UUID,
        current_message: str,
        limit: int = 10,
    ) -> dict[str, Any]:
        """
        Get relevant learning context for a conversation.
        
        Uses semantic search to find relevant:
        - Vocabulary items
        - Grammar rules
        - Past errors
        
        Args:
            user_id: The user's unique identifier
            current_message: The current user message (for semantic matching)
            limit: Maximum items per category
            
        Returns:
            Dictionary containing relevant context:
            {
                "vocabulary": [...],
                "errors": [...],
                "rules": [...],
            }
        """
        ...
    
    @abstractmethod
    async def semantic_search(
        self,
        query: str,
        limit: int = 10,
    ) -> list[dict[str, Any]]:
        """
        Perform semantic search across the knowledge graph.
        
        Args:
            query: Natural language query
            limit: Maximum results to return
            
        Returns:
            List of matching items with relevance scores
        """
        ...
    
    # ==========================================
    # User Management
    # ==========================================
    
    @abstractmethod
    async def ensure_user_exists(
        self,
        user_id: UUID,
    ) -> None:
        """
        Ensure a user node exists in the graph.
        
        Creates the User node if it doesn't exist.
        Idempotent operation.
        
        Args:
            user_id: The user's unique identifier
        """
        ...
