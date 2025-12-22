"""
Tests for User entity.

User represents a language learner with native and target languages.
Users progress through CEFR levels (A1-C2).
"""

from __future__ import annotations

import pytest

from src.core.domain.value_objects import CEFRLevel, Language
from src.core.exceptions import InvalidLanguagePairError, InvalidLevelChangeError
from tests.conftest import MakeUser


class TestUserCreation:
    """Tests for User instantiation."""

    def test_user_with_valid_data(
        self, make_user: MakeUser
    ) -> None:
        """A valid user can be created with factory defaults."""
        user = make_user()

        assert user.native_lang.code == "fr"
        assert user.target_lang.code == "en"
        assert user.level == CEFRLevel.B1

    def test_user_with_custom_languages(
        self, make_user: MakeUser
    ) -> None:
        """A user can be created with custom languages."""
        user = make_user(
            native_lang=Language("zz"),
            target_lang=Language("xy"),
            level=CEFRLevel.A2
        )

        assert user.native_lang.code == "zz"
        assert user.target_lang.code == "xy"
        assert user.level == CEFRLevel.A2

    def test_cannot_learn_native_language(
        self, make_user: MakeUser
    ) -> None:
        """User cannot have same native and target language."""
        with pytest.raises(InvalidLanguagePairError):
            make_user(
                native_lang=Language("fr"),
                target_lang=Language("fr")
            )


class TestUserCorrectNativeLanguage:
    """Tests for correcting the native language."""

    def test_correct_native_language_success(
        self, make_user: MakeUser
    ) -> None:
        """Native language can be corrected to a different language."""
        user = make_user(
            native_lang=Language("fr"),
            target_lang=Language("en")
        )

        user.correct_native_language(Language("es"))

        assert user.native_lang.code == "es"

    def test_correct_native_language_same_as_target_raises(
        self, make_user: MakeUser
    ) -> None:
        """Cannot correct native language to be same as target."""
        user = make_user(
            native_lang=Language("fr"),
            target_lang=Language("en")
        )

        with pytest.raises(InvalidLanguagePairError):
            user.correct_native_language(Language("en"))


class TestUserSwitchLearningGoal:
    """Tests for switching the target language."""

    def test_switch_learning_goal_success(
        self, make_user: MakeUser
    ) -> None:
        """Target language can be switched to a different language."""
        user = make_user(
            native_lang=Language("fr"),
            target_lang=Language("en")
        )

        user.switch_learning_goal(Language("de"))

        assert user.target_lang.code == "de"

    def test_switch_learning_goal_same_as_native_raises(
        self, make_user: MakeUser
    ) -> None:
        """Cannot switch target language to be same as native."""
        user = make_user(
            native_lang=Language("fr"),
            target_lang=Language("en")
        )

        with pytest.raises(InvalidLanguagePairError):
            user.switch_learning_goal(Language("fr"))


class TestUserAssessLevel:
    """Tests for updating the user's proficiency level."""

    def test_assess_level_success(
        self, make_user: MakeUser
    ) -> None:
        """Level can be updated to the next adjacent level."""
        user = make_user(level=CEFRLevel.A1)

        user.assess_level(CEFRLevel.A2)

        assert user.level == CEFRLevel.A2

    def test_assess_level_same_as_current_raises(
        self, make_user: MakeUser
    ) -> None:
        """Cannot update level to the same value."""
        user = make_user(level=CEFRLevel.B1)

        with pytest.raises(InvalidLevelChangeError):
            user.assess_level(CEFRLevel.B1)

    def test_assess_level_not_adjacant_raises(self, make_user: MakeUser) -> None:
        """Level cannot be updated to non-adjacent level."""
        user = make_user(level=CEFRLevel.A1)
        
        with pytest.raises(InvalidLevelChangeError):
            user.assess_level(CEFRLevel.B1)

   