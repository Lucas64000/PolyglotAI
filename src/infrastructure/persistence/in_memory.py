"""
In-Memory Repository Implementations

For testing and development without database dependencies.
"""

from datetime import datetime
from typing import Dict
from uuid import UUID

from src.core.domain.entities import UserProfile, VocabularyItem
from src.core.domain.value_objects import CEFRLevel, Language, LanguagePair


class InMemoryUserRepository:
    """
    In-memory implementation of UserRepository.
    
    Stores user profiles in a dictionary.
    For testing and development only.
    """
    
    def __init__(self) -> None:
        self._users: Dict[UUID, UserProfile] = {}
    
    async def get_by_id(self, user_id: UUID) -> UserProfile | None:
        """Get user by ID."""
        return self._users.get(user_id)
    
    async def save(self, user: UserProfile) -> None:
        """Save or update user."""
        self._users[user.id] = user
    
    async def update(self, user: UserProfile) -> None:
        """Update existing user."""
        if user.id not in self._users:
            raise ValueError(f"User {user.id} not found")
        self._users[user.id] = user
    
    async def delete(self, user_id: UUID) -> bool:
        """Delete user by ID. Returns True if deleted, False if not found."""
        if user_id in self._users:
            del self._users[user_id]
            return True
        return False
    
    async def exists(self, user_id: UUID) -> bool:
        """Check if user exists."""
        return user_id in self._users
    
    # Helper for testing
    def add_test_user(
        self,
        user_id: UUID,
        native: str = "fr",
        target: str = "en",
        level: CEFRLevel = CEFRLevel.B1,
    ) -> UserProfile:
        """Add a test user (synchronous for test setup)."""
        user = UserProfile(
            id=user_id,
            language_pair=LanguagePair(
                source=Language(native),
                target=Language(target),
            ),
            current_level=level,
            created_at=datetime.now(),
        )
        self._users[user_id] = user
        return user


class InMemoryVocabularyRepository:
    """
    In-memory implementation of VocabularyRepository.
    
    Stores vocabulary items per user in nested dictionaries.
    For testing and development only.
    """
    
    def __init__(self) -> None:
        # Structure: {user_id: {term: VocabularyItem}}
        self._vocabulary: Dict[UUID, Dict[str, VocabularyItem]] = {}
    
    async def get_by_term(
        self,
        user_id: UUID,
        term: str,
    ) -> VocabularyItem | None:
        """Get vocabulary item by term for a user."""
        user_vocab = self._vocabulary.get(user_id, {})
        return user_vocab.get(term.lower())
    
    async def save(
        self,
        user_id: UUID,
        item: VocabularyItem,
    ) -> None:
        """Save vocabulary item for a user."""
        if user_id not in self._vocabulary:
            self._vocabulary[user_id] = {}
        self._vocabulary[user_id][item.term.lower()] = item
    
    async def get_all_for_user(
        self,
        user_id: UUID,
    ) -> list[VocabularyItem]:
        """Get all vocabulary for a user."""
        user_vocab = self._vocabulary.get(user_id, {})
        return list(user_vocab.values())
    
    async def get_for_review(
        self,
        user_id: UUID,
        limit: int = 10,
    ) -> list[VocabularyItem]:
        """Get items needing review (low stability or not recently reviewed)."""
        user_vocab = self._vocabulary.get(user_id, {})
        items = list(user_vocab.values())
        
        # Sort by stability (ascending) - least stable first
        items.sort(key=lambda x: x.stability)
        
        return items[:limit]
    
    async def update_mastery(
        self,
        user_id: UUID,
        term: str,
        correct: bool,
    ) -> None:
        """Update item mastery after review."""
        item = await self.get_by_term(user_id, term)
        if item is None:
            return
        
        # Simple SRS-like update
        if correct:
            new_stability = min(1.0, item.stability + 0.2)
        else:
            new_stability = max(0.1, item.stability - 0.1)
        
        # Create updated item (entities are immutable by convention)
        updated = VocabularyItem(
            term=item.term,
            definition=item.definition,
            language=item.language,
            part_of_speech=item.part_of_speech,
            context_usage=item.context_usage,
            stability=new_stability,
            last_reviewed=datetime.now(),
        )
        
        await self.save(user_id, updated)
    
    async def count_for_user(self, user_id: UUID) -> int:
        """Count vocabulary items for a user."""
        return len(self._vocabulary.get(user_id, {}))
    
    async def delete(
        self,
        user_id: UUID,
        term: str,
    ) -> None:
        """Delete a vocabulary item."""
        user_vocab = self._vocabulary.get(user_id, {})
        term_lower = term.lower()
        if term_lower in user_vocab:
            del user_vocab[term_lower]
