"""
Fixtures de test pour les modèles
Données d'exemple prêtes à l'emploi pour les tests et démos
"""

from typing import List
from uuid import uuid4

from src.agents.core.enums import (
    CECRLevel,
    Language,
    Role,
)
from src.models.conversation_model import (
    Conversation,
    Message,
    Correction,
)
from src.models.user_model import User


# ============================================================================
# UTILISATEURS DE TEST
# ============================================================================

# Utilisateur français apprenant l'anglais
sample_user_french_to_english = User(
    id=uuid4(),
    name="Lucas",
    native_language=Language.FRENCH,
    target_language=Language.ENGLISH,
    current_level=CECRLevel.B1,
    initial_level=CECRLevel.A2,
)

# Utilisateur anglais apprenant le français
sample_user_english_to_french = User(
    id=uuid4(),
    name="Emma",
    native_language=Language.ENGLISH,
    target_language=Language.FRENCH,
    current_level=CECRLevel.A2,
    initial_level=CECRLevel.A1,
)

# Utilisateur beginner 
sample_user_beginner = User(
    id=uuid4(),
    name="Maria",
    native_language=Language.FRENCH,
    target_language=Language.ENGLISH,
    current_level=CECRLevel.A1,
)

# ============================================================================
# CONVERSATIONS DE TEST
# ============================================================================

sample_conversation_active = Conversation(
    id=uuid4(),
    user_id=sample_user_french_to_english.id,
    title="Practice Session - Past Tenses",
)

sample_conversation_archived = Conversation(
    id=uuid4(),
    user_id=sample_user_english_to_french.id,
    title="Daily Practice - November 5",
)


# ============================================================================
# MESSAGES DE TEST
# ============================================================================

sample_message_with_errors = Message(
    id=uuid4(),
    conversation_id=sample_conversation_active.id,
    user_id=sample_user_french_to_english.id,
    content="I go to school yesterday and I see a car red big, it was impressive.",
    role=Role.USER,
)

sample_message_correct = Message(
    id=uuid4(),
    conversation_id=sample_conversation_active.id,
    user_id=sample_user_french_to_english.id,
    content="Yesterday I went to school and ate a big breakfast. It was delicious!",
    role=Role.USER,
)

sample_message_agent_response = Message(
    id=uuid4(),
    conversation_id=sample_conversation_active.id,
    user_id=sample_user_french_to_english.id,
    content="Great job! We say 'I WENT to school yesterday' and 'I ATE a big breakfast'. What did you have for breakfast?",
    role=Role.ASSISTANT,
)


# ============================================================================
# CORRECTIONS DE TEST
# ============================================================================

sample_correction_verb_tense = Correction(
    id=uuid4(),
    message_id=sample_message_with_errors.id,
    original="I go",
    corrected="I went",
    start_index=0,
    end_index=4,
)


# ============================================================================
# HISTORIQUES DE CONVERSATION DE TEST
# ============================================================================

sample_conversation_history = [
    Message(
        id=uuid4(),
        conversation_id=sample_conversation_active.id,
        user_id=sample_user_french_to_english.id,
        content="Hello! How are you today?",
        role=Role.USER,
    ),
    Message(
        id=uuid4(),
        conversation_id=sample_conversation_active.id,
        user_id=sample_user_french_to_english.id,
        content="Hi! I'm doing well, thank you. I'm practicing English because I want to improve my conversation skills. How about you?",
        role=Role.ASSISTANT,
    ),
    Message(
        id=uuid4(),
        conversation_id=sample_conversation_active.id,
        user_id=sample_user_french_to_english.id,
        content="I'm good too. I like learning languages. Yesterday I go to the cinema.",
        role=Role.USER,
    ),
    Message(
        id=uuid4(),
        conversation_id=sample_conversation_active.id,
        user_id=sample_user_french_to_english.id,
        content="Great! We say 'I went to the cinema yesterday.' What movie did you see?",
        role=Role.ASSISTANT,
    )
]

# Historique plus court pour tests rapides
sample_short_history = [
    Message(
        id=uuid4(),
        conversation_id=sample_conversation_active.id,
        user_id=sample_user_french_to_english.id,
        content="Hello! How are you?",
        role=Role.USER,
    ),
    Message(
        id=uuid4(),
        conversation_id=sample_conversation_active.id,
        user_id=sample_user_french_to_english.id,
        content="Hi! I'm fine, thank you. And you?",
        role=Role.ASSISTANT,
    )
]

# Historique vide pour tests
sample_empty_history: List[Message] = []

# Liste de tous les utilisateurs de test
test_users = [
    sample_user_french_to_english,
    sample_user_english_to_french,
    sample_user_beginner
]

# Liste de toutes les conversations de test
test_conversations = [
    sample_conversation_active,
    sample_conversation_archived
]

# Liste de tous les messages de test
test_messages = [
    sample_message_with_errors,
    sample_message_correct,
    sample_message_agent_response
]

# Liste de tous les historiques de test
test_histories = [
    sample_conversation_history,
    sample_short_history,
    sample_empty_history
]
