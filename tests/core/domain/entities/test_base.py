"""
Tests for the base Entity class.
"""

from datetime import datetime, timezone
from uuid import uuid4

from src.core.domain.entities.base import Entity


class ConcreteEntity(Entity):
    """Concrete implementation of Entity for testing purposes."""
    pass


class AnotherEntity(Entity):
    """Another concrete implementation to test type checking."""
    pass


class TestEntityIdentity:
    """Tests for Entity identity semantics."""

    def test_entities_with_same_id_are_equal(self) -> None:
        """Two entities of the same type with the same ID should be equal."""
        shared_id = uuid4()
        now = datetime.now(timezone.utc)
        
        entity1 = ConcreteEntity(_id=shared_id, _created_at=now)
        entity2 = ConcreteEntity(_id=shared_id, _created_at=now)
        
        assert entity1 == entity2

    def test_entities_with_different_ids_are_not_equal(self) -> None:
        """Two entities with different IDs should not be equal."""
        now = datetime.now(timezone.utc)
        
        entity1 = ConcreteEntity(_id=uuid4(), _created_at=now)
        entity2 = ConcreteEntity(_id=uuid4(), _created_at=now)
        
        assert entity1 != entity2

    def test_entities_of_different_types_are_not_equal(self) -> None:
        """Two entities of different types are never equal, even with same ID."""
        shared_id = uuid4()
        now = datetime.now(timezone.utc)
        
        entity1 = ConcreteEntity(_id=shared_id, _created_at=now)
        entity2 = AnotherEntity(_id=shared_id, _created_at=now)
        
        assert entity1 != entity2

class TestEntityHashing:
    """Tests for Entity hashing behavior."""

    def test_entity_is_hashable(self) -> None:
        """Entities should be hashable for use in sets and dicts."""
        entity = ConcreteEntity(
            _id=uuid4(), 
            _created_at=datetime.now(timezone.utc)
        )
        
        # Should not raise
        hash(entity)

    def test_entities_with_same_id_have_same_hash(self) -> None:
        """Equal entities should have the same hash."""
        shared_id = uuid4()
        now = datetime.now(timezone.utc)
        
        entity1 = ConcreteEntity(_id=shared_id, _created_at=now)
        entity2 = ConcreteEntity(_id=shared_id, _created_at=now)
        
        assert hash(entity1) == hash(entity2)

    def test_entity_can_be_used_in_set(self) -> None:
        """Entities should work correctly in sets."""
        shared_id = uuid4()
        now = datetime.now(timezone.utc)
        
        entity1 = ConcreteEntity(_id=shared_id, _created_at=now)
        entity2 = ConcreteEntity(_id=shared_id, _created_at=now)
        entity3 = ConcreteEntity(_id=uuid4(), _created_at=now)
        
        entity_set = {entity1, entity2, entity3}
        
        # entity1 and entity2 are the same (same ID), so set should have 2 items
        assert len(entity_set) == 2

    def test_entity_can_be_used_as_dict_key(self) -> None:
        """Entities should work correctly as dictionary keys."""
        entity = ConcreteEntity(
            _id=uuid4(), 
            _created_at=datetime.now(timezone.utc)
        )
        
        data = {entity: "value"}
        
        assert data[entity] == "value"

    def test_equal_entities_access_same_dict_value(self) -> None:
        """Equal entities should access the same dictionary value."""
        shared_id = uuid4()
        now = datetime.now(timezone.utc)
        
        entity1 = ConcreteEntity(_id=shared_id, _created_at=now)
        entity2 = ConcreteEntity(_id=shared_id, _created_at=now)
        
        data = {entity1: "value"}
        
        assert data[entity2] == "value"
