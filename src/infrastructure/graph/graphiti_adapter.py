"""
Graphiti Adapter

Implements the GraphMemory port using graphiti_core.
This is the bridge between our domain model and the graph database.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import TYPE_CHECKING, Any
from uuid import UUID

from pydantic import BaseModel

if TYPE_CHECKING:
    from graphiti_core import Graphiti

from src.core.domain.entities import (
    GrammarRule as DomainGrammarRule,
    UserError,
    VocabularyItem,
)
from src.infrastructure.config.ai import (
    AIProviderConfig,
    AzureOpenAIConfig,
    OllamaConfig,
    OpenAIConfig,
)
from src.infrastructure.config.database import Neo4jConfig
from src.infrastructure.graph.mappers import VocabularyMapper


class GraphitiAdapter:
    """
    Adapter implementing GraphMemory port using Graphiti.
    
    This class:
    - Receives AI config and Neo4j config
    - Creates Graphiti-native LLM and Embedder clients internally
    - Manages the Graphiti client lifecycle
    - Uses Graphiti's automatic extraction via add_episode()
    - Handles semantic search and context retrieval
    - Supports custom entity_types and edge_types for domain-specific extraction
    
    Graphiti requires its own client types (OpenAIGenericClient, OpenAIEmbedder),
    so we create them internally based on the AI provider configuration.
    """
    
    def __init__(
        self,
        ai_config: AIProviderConfig,
        neo4j_config: Neo4jConfig,
        entity_types: dict[str, type[BaseModel]] | None = None,
        edge_types: dict[str, type[BaseModel]] | None = None,
    ) -> None:
        """
        Initialize the Graphiti adapter.
        
        Args:
            ai_config: AI provider configuration (to create Graphiti-native clients)
            neo4j_config: Neo4j configuration (secrets extracted here)
            entity_types: Custom entity types for extraction (Pydantic models)
            edge_types: Custom edge types for extraction (Pydantic models)
        """
        self._ai_config = ai_config
        # Extract config values - secrets are extracted here, not exposed
        self._neo4j_uri = neo4j_config.uri
        self._neo4j_user = neo4j_config.user
        self._neo4j_password = neo4j_config.password.get_secret_value()
        self._client: "Graphiti | None" = None
        self._initialized = False
        
        # Custom ontology for domain-specific extraction
        self._entity_types = entity_types
        self._edge_types = edge_types
    
    def _create_graphiti_llm_client(self) -> Any:
        """
        Create Graphiti-native LLM client based on AI config.
        
        Graphiti requires its own LLMClient types, so we create them
        based on our provider configuration.
        """
        from graphiti_core.llm_client.config import LLMConfig
        from graphiti_core.llm_client.openai_generic_client import OpenAIGenericClient
        
        config = self._ai_config
        
        if isinstance(config, OllamaConfig):
            llm_config = LLMConfig(
                api_key="ollama",  # Ollama doesn't need a real API key
                model=config.chat_model,
                small_model=config.chat_model,
                base_url=config.openai_compatible_url,
            )
            return OpenAIGenericClient(config=llm_config)
        
        elif isinstance(config, OpenAIConfig):
            from graphiti_core.llm_client import OpenAIClient
            
            llm_config = LLMConfig(
                api_key=config.api_key.get_secret_value(),
                model=config.chat_model,
                small_model=config.chat_model,
            )
            return OpenAIClient(config=llm_config)
        
        elif isinstance(config, AzureOpenAIConfig):
            from openai import AsyncOpenAI
            from graphiti_core.llm_client.azure_openai_client import AzureOpenAILLMClient
            
            # Azure v1 API endpoint
            azure_client = AsyncOpenAI(
                base_url=f"{config.endpoint}/openai/v1/",
                api_key=config.api_key.get_secret_value(),
            )
            
            llm_config = LLMConfig(
                model=config.chat_deployment,
                small_model=config.chat_deployment,
            )
            return AzureOpenAILLMClient(azure_client=azure_client, config=llm_config)
        
        else:
            raise ValueError(f"Unsupported AI provider config: {type(config).__name__}")
    
    def _create_graphiti_embedder(self) -> Any:
        """
        Create Graphiti-native Embedder client based on AI config.
        """
        from graphiti_core.embedder.openai import OpenAIEmbedder, OpenAIEmbedderConfig
        
        config = self._ai_config
        
        if isinstance(config, OllamaConfig):
            embedder_config = OpenAIEmbedderConfig(
                api_key="ollama",
                embedding_model=config.embedding_model,
                embedding_dim=768,  # nomic-embed-text default
                base_url=config.openai_compatible_url,
            )
            return OpenAIEmbedder(config=embedder_config)
        
        elif isinstance(config, OpenAIConfig):
            embedder_config = OpenAIEmbedderConfig(
                api_key=config.api_key.get_secret_value(),
                embedding_model=config.embedding_model,
            )
            return OpenAIEmbedder(config=embedder_config)
        
        elif isinstance(config, AzureOpenAIConfig):
            from openai import AsyncOpenAI
            from graphiti_core.embedder.azure_openai import AzureOpenAIEmbedderClient
            
            azure_client = AsyncOpenAI(
                base_url=f"{config.endpoint}/openai/v1/",
                api_key=config.api_key.get_secret_value(),
            )
            
            return AzureOpenAIEmbedderClient(
                azure_client=azure_client,
                model=config.embedding_deployment,
            )
        
        else:
            raise ValueError(f"Unsupported AI provider config: {type(config).__name__}")
    
    async def _get_client(self) -> Any:
        """
        Get or create the Graphiti client.
        
        Lazy initialization to avoid async in __init__.
        Returns Any to avoid type issues with conditional imports.
        """
        if self._client is None:
            # Import at runtime to allow graceful fallback if not installed
            try:
                from graphiti_core import Graphiti as GraphitiClient
            except ImportError as e:
                raise ImportError(
                    "graphiti_core is required but not installed. "
                    "Install it with: pip install graphiti-core"
                ) from e
            
            # Create Graphiti-native clients
            llm_client = self._create_graphiti_llm_client()
            embedder = self._create_graphiti_embedder()
            
            # Create Graphiti client with native clients
            self._client = GraphitiClient(
                uri=self._neo4j_uri,
                user=self._neo4j_user,
                password=self._neo4j_password,
                llm_client=llm_client,
                embedder=embedder,
            )
            
            # Build indices if not already done
            if not self._initialized:
                await self._client.build_indices_and_constraints()
                self._initialized = True
        
        return self._client
    
    def _get_episode_type(self, type_name: str) -> Any:
        """Get EpisodeType enum value by name at runtime."""
        from graphiti_core.nodes import EpisodeType
        return getattr(EpisodeType, type_name)
    
    async def close(self) -> None:
        """Close the Graphiti client connection."""
        if self._client:
            await self._client.close()
            self._client = None
    
    # ==========================================
    # Episode Management (Graphiti's main API)
    # ==========================================
    
    async def add_conversation_episode(
        self,
        user_id: UUID,
        user_message: str,
        tutor_response: str,
        session_id: UUID | None = None,
    ) -> None:
        """
        Add a conversation turn as an episode.
        
        Graphiti will automatically extract entities (vocabulary, errors, etc.)
        based on the conversation content and the custom ontology.
        
        Args:
            user_id: User identifier (used as group_id)
            user_message: What the learner said
            tutor_response: What the tutor replied
            session_id: Optional session identifier
        """
        client = await self._get_client()
        
        # Format conversation for Graphiti
        episode_body = f"Learner: {user_message}\nTutor: {tutor_response}"
        
        await client.add_episode(
            name=f"conversation_{session_id or user_id}",
            episode_body=episode_body,
            source=self._get_episode_type("message"),
            source_description="Language learning conversation",
            reference_time=datetime.now(timezone.utc),
            group_id=str(user_id),
            entity_types=self._entity_types,
            edge_types=self._edge_types,
        )
    
    # ==========================================
    # Vocabulary Operations
    # ==========================================
    
    async def store_vocabulary(
        self,
        user_id: UUID,
        vocabulary: VocabularyItem,
    ) -> None:
        """
        Store a vocabulary item in the graph.
        
        Uses Graphiti's add_episode with structured data.
        """
        client = await self._get_client()
        
        # Convert to graph format (for future use with custom nodes)
        _vocab_node, _definition_node = VocabularyMapper.to_graph_nodes(vocabulary)
        
        # Create episode for the vocabulary learning
        episode_body = (
            f"The learner encountered the word '{vocabulary.term}' "
            f"({vocabulary.language.name}). "
            f"Definition: {vocabulary.definition}."
        )
        if vocabulary.context_example:
            episode_body += f" Example: {vocabulary.context_example}"
        
        await client.add_episode(
            name=f"vocabulary_{vocabulary.term}",
            episode_body=episode_body,
            source=self._get_episode_type("text"),
            source_description="Vocabulary learning entry",
            reference_time=datetime.now(timezone.utc),
            group_id=str(user_id),
            entity_types=self._entity_types,
            edge_types=self._edge_types,
        )
    
    async def get_vocabulary(
        self,
        user_id: UUID,
        term: str,
    ) -> VocabularyItem | None:
        """Retrieve a vocabulary item by term."""
        client = await self._get_client()
        
        # Search for the term
        results = await client.search(
            query=term,
            group_ids=[str(user_id)],
            num_results=1,
        )
        
        if not results:
            return None
        
        # TODO: Convert search result to VocabularyItem
        # This depends on Graphiti's result structure
        return None
    
    async def get_vocabulary_for_review(
        self,
        user_id: UUID,
        limit: int = 10,
    ) -> list[VocabularyItem]:
        """Get vocabulary items needing review based on SRS."""
        # TODO: Implement with custom Cypher query for SRS logic
        return []
    
    async def update_vocabulary_mastery(
        self,
        user_id: UUID,
        term: str,
        correct: bool,
    ) -> None:
        """Update mastery after review."""
        # Record the review as an episode
        client = await self._get_client()
        
        result = "correctly" if correct else "incorrectly"
        episode_body = f"The learner reviewed the word '{term}' and recalled it {result}."
        
        await client.add_episode(
            name=f"review_{term}",
            episode_body=episode_body,
            source=self._get_episode_type("text"),
            source_description="Vocabulary review session",
            reference_time=datetime.now(timezone.utc),
            group_id=str(user_id),
            entity_types=self._entity_types,
            edge_types=self._edge_types,
        )
    
    # ==========================================
    # Error Tracking Operations
    # ==========================================
    
    async def store_error(
        self,
        user_id: UUID,
        error: UserError,
    ) -> None:
        """
        Store a user error in the graph.
        
        Records the error as an episode for Graphiti to process.
        """
        client = await self._get_client()
        
        episode_body = (
            f"The learner made an error: wrote '{error.wrong_form}' "
            f"instead of '{error.correction}'. "
            f"Error type: {error.error_type.value}."
        )
        if error.explanation:
            episode_body += f" Explanation: {error.explanation}"
        
        await client.add_episode(
            name=f"error_{error.wrong_form}",
            episode_body=episode_body,
            source=self._get_episode_type("text"),
            source_description="Learner error tracking",
            reference_time=datetime.now(timezone.utc),
            group_id=str(user_id),
            entity_types=self._entity_types,
            edge_types=self._edge_types,
        )
    
    async def get_recurring_errors(
        self,
        user_id: UUID,
        limit: int = 5,
    ) -> list[UserError]:
        """Get most common errors."""
        client = await self._get_client()
        
        # Search for error-related content
        _results = await client.search(
            query="learner made error mistake wrong",
            group_ids=[str(user_id)],
            num_results=limit,
        )
        
        # TODO: Convert results to UserError entities
        return []
    
    async def increment_error_count(
        self,
        user_id: UUID,
        wrong_form: str,
    ) -> None:
        """Increment error occurrence count by recording another occurrence."""
        client = await self._get_client()
        
        episode_body = f"The learner repeated the error '{wrong_form}' again."
        
        await client.add_episode(
            name=f"error_repeat_{wrong_form}",
            episode_body=episode_body,
            source=self._get_episode_type("text"),
            source_description="Repeated error occurrence",
            reference_time=datetime.now(timezone.utc),
            group_id=str(user_id),
            entity_types=self._entity_types,
            edge_types=self._edge_types,
        )
    
    # ==========================================
    # Grammar Rule Operations
    # ==========================================
    
    async def store_grammar_rule(
        self,
        rule: DomainGrammarRule,
    ) -> None:
        """Store a grammar rule."""
        client = await self._get_client()
        
        episode_body = (
            f"Grammar rule: {rule.rule_name}. "
            f"Language: {rule.language.name}. "
            f"Explanation: {rule.explanation}."
        )
        if rule.examples:
            episode_body += f" Examples: {', '.join(rule.examples)}"
        
        await client.add_episode(
            name=f"rule_{rule.rule_name}",
            episode_body=episode_body,
            source=self._get_episode_type("text"),
            source_description="Grammar rule definition",
            reference_time=datetime.now(timezone.utc),
            group_id="global",  # Rules are shared across users
            entity_types=self._entity_types,
            edge_types=self._edge_types,
        )
    
    async def get_grammar_rule(
        self,
        rule_name: str,
    ) -> DomainGrammarRule | None:
        """Get grammar rule by name."""
        client = await self._get_client()
        
        _results = await client.search(
            query=f"grammar rule {rule_name}",
            num_results=1,
        )
        
        # TODO: Convert to domain entity
        return None
    
    # ==========================================
    # Context & Search Operations
    # ==========================================
    
    async def get_learning_context(
        self,
        user_id: UUID,
        current_message: str,
        limit: int = 10,
    ) -> dict[str, Any]:
        """
        Get relevant learning context for conversation.
        
        Uses Graphiti's hybrid search to find relevant:
        - Vocabulary the user knows
        - Recent errors
        - Applicable grammar rules
        """
        client = await self._get_client()
        
        # Perform semantic search
        results = await client.search(
            query=current_message,
            group_ids=[str(user_id)],
            num_results=limit,
        )
        
        # Categorize results (simplified - would need proper result parsing)
        context: dict[str, Any] = {
            "vocabulary": [],
            "errors": [],
            "rules": [],
            "raw_results": [str(r) for r in results] if results else [],
        }
        
        return context
    
    async def semantic_search(
        self,
        query: str,
        limit: int = 10,
    ) -> list[dict[str, Any]]:
        """Perform semantic search across the graph."""
        client = await self._get_client()
        
        results = await client.search(
            query=query,
            num_results=limit,
        )
        
        # Convert results to dicts
        return [{"result": str(r)} for r in results] if results else []
    
    # ==========================================
    # User Management
    # ==========================================
    
    async def ensure_user_exists(
        self,
        user_id: UUID,
    ) -> None:
        """
        Ensure user context exists in the graph.
        
        With Graphiti, users are implicitly created via group_id
        when adding episodes. This is a no-op but kept for interface
        compatibility.
        """
        # Graphiti handles this via group_id in add_episode
        # No explicit user creation needed
        pass
