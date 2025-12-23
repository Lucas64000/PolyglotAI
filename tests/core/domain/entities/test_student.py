"""
Tests for Student entity.

Student represents a language learner with native and target languages.
Students progress through CEFR levels (A1-C2).
"""

from __future__ import annotations

import pytest

from src.core.domain.value_objects import CEFRLevel, Language
from src.core.exceptions import InvalidLanguagePairError, InvalidLevelChangeError

from tests.conftest import MakeStudent


class TestStudentCreation:
    """Tests for student instantiation."""

    def test_student_with_valid_data(
        self, make_student: MakeStudent
    ) -> None:
        """A valid student can be created with factory defaults."""
        student = make_student()

        assert student.native_lang.code == "fr"
        assert student.target_lang.code == "en"
        assert student.level == CEFRLevel.B1

    def test_student_with_custom_languages(
        self, make_student: MakeStudent
    ) -> None:
        """Students can be created with custom languages."""
        student = make_student(
            native_lang=Language("zz"),
            target_lang=Language("xy"),
            level=CEFRLevel.A2
        )

        assert student.native_lang.code == "zz"
        assert student.target_lang.code == "xy"
        assert student.level == CEFRLevel.A2

    def test_student_cannot_learn_native_language(
        self, make_student: MakeStudent
    ) -> None:
        """Students cannot have same native and target language."""
        with pytest.raises(InvalidLanguagePairError):
            make_student(
                native_lang=Language("fr"),
                target_lang=Language("fr")
            )


class TeststudentCorrectNativeLanguage:
    """Tests for correcting the native language."""

    def test_correct_native_language_success(
        self, make_student: MakeStudent
    ) -> None:
        """Native language can be corrected to a different language."""
        student = make_student(
            native_lang=Language("fr"),
            target_lang=Language("en")
        )

        student.correct_native_language(Language("es"))

        assert student.native_lang.code == "es"

    def test_correct_native_language_same_as_target_raises(
        self, make_student: MakeStudent
    ) -> None:
        """Cannot correct native language to be same as target."""
        student = make_student(
            native_lang=Language("fr"),
            target_lang=Language("en")
        )

        with pytest.raises(InvalidLanguagePairError):
            student.correct_native_language(Language("en"))


class TeststudentSwitchLearningGoal:
    """Tests for switching the target language."""

    def test_switch_learning_goal_success(
        self, make_student: MakeStudent
    ) -> None:
        """Target language can be switched to a different language."""
        student = make_student(
            native_lang=Language("fr"),
            target_lang=Language("en")
        )

        student.switch_learning_goal(Language("de"))

        assert student.target_lang.code == "de"

    def test_switch_learning_goal_same_as_native_raises(
        self, make_student: MakeStudent
    ) -> None:
        """Cannot switch target language to be same as native."""
        student = make_student(
            native_lang=Language("fr"),
            target_lang=Language("en")
        )

        with pytest.raises(InvalidLanguagePairError):
            student.switch_learning_goal(Language("fr"))


class TeststudentAssessLevel:
    """Tests for updating the student's proficiency level."""

    def test_assess_level_success(
        self, make_student: MakeStudent
    ) -> None:
        """Level can be updated to the next adjacent level."""
        student = make_student(level=CEFRLevel.A1)

        student.assess_level(CEFRLevel.A2)

        assert student.level == CEFRLevel.A2

    def test_assess_level_same_as_current_raises(
        self, make_student: MakeStudent
    ) -> None:
        """Cannot update level to the same value."""
        student = make_student(level=CEFRLevel.B1)

        with pytest.raises(InvalidLevelChangeError):
            student.assess_level(CEFRLevel.B1)

    def test_assess_level_not_adjacant_raises(self, make_student: MakeStudent) -> None:
        """Level cannot be updated to non-adjacent level."""
        student = make_student(level=CEFRLevel.A1)
        
        with pytest.raises(InvalidLevelChangeError):
            student.assess_level(CEFRLevel.B1)

   