"""
Tests for VocabularyItem entity.

VocabularyItem represents the link between a User and a learned word (Lexeme).
It tracks review progress and last review timestamp.
"""

from __future__ import annotations

from datetime import datetime, timezone, timedelta
from uuid import uuid4

from src.core.domain.value_objects import (
    Language,
    PartOfSpeech,
)
from tests.conftest import MakeVocab


class TestVocabularyItemCreation:
    """Tests for VocabularyItem instantiation."""

    def test_vocabulary_item_with_factory_defaults(
        self, make_vocab: MakeVocab
    ) -> None:
        """A vocabulary item can be created with factory defaults."""
        vocab = make_vocab()

        assert vocab.review_count == 1
        assert vocab.lexeme is not None
        assert vocab.user_id is not None

    def test_vocabulary_item_with_custom_lexeme(
        self, make_vocab: MakeVocab
    ) -> None:
        """A vocabulary item can be created with a custom lexeme."""
        vocab = make_vocab(
            term="manger",
            language=Language("fr"),
            pos=PartOfSpeech.VERB,
            definition="to eat"
        )

        assert vocab.lexeme.lemma.term == "manger"
        assert vocab.lexeme.lemma.language == Language("fr")
        assert vocab.lexeme.lemma.pos == PartOfSpeech.VERB
        assert vocab.lexeme.definition == "to eat"

    def test_vocabulary_item_has_user_id(
        self, make_vocab: MakeVocab
    ) -> None:
        """Vocabulary items are linked to a user."""
        user_id = uuid4()
        vocab = make_vocab(user_id=user_id)

        assert vocab.user_id == user_id

    def test_vocabulary_item_initial_review_count(
        self, make_vocab: MakeVocab
    ) -> None:
        """New vocabulary items start with review count of 1."""
        vocab = make_vocab()

        assert vocab.review_count == 1


class TestVocabularyItemReview:
    """Tests for the mark_as_reviewed method."""

    def test_mark_as_reviewed_increases_count(
        self, make_vocab: MakeVocab
    ) -> None:
        """Reviewing increases the review count."""
        vocab = make_vocab()
        initial_count = vocab.review_count

        vocab.mark_as_reviewed(datetime.now(timezone.utc))

        assert vocab.review_count == initial_count + 1

    def test_mark_as_reviewed_updates_timestamp(
        self, make_vocab: MakeVocab
    ) -> None:
        """Reviewing updates the last reviewed timestamp."""
        initial_time = datetime.now(timezone.utc)
        vocab = make_vocab(now=initial_time)

        later_time = initial_time + timedelta(hours=1)
        vocab.mark_as_reviewed(later_time)

        assert vocab.last_reviewed_at == later_time

    def test_multiple_reviews_increment_count(
        self, make_vocab: MakeVocab
    ) -> None:
        """Multiple reviews increment the count correctly."""
        vocab = make_vocab()
        now = datetime.now(timezone.utc)

        vocab.mark_as_reviewed(now + timedelta(hours=1))
        vocab.mark_as_reviewed(now + timedelta(hours=2))
        vocab.mark_as_reviewed(now + timedelta(hours=3))

        # Started at 1, reviewed 3 times
        assert vocab.review_count == 4