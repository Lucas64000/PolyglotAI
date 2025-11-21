
from src.models.conversation_model import Message
from src.models.user_model import User
from src.services.llm.providers.provider_interface import BaseLLMProvider
from src.services.memory.strategies.strategy_interface import BaseMemoryStrategy
from .agent_interface import BaseAgent

from src.core.types import TMessage, TResponse
from src.core.enums import Role
from uuid import uuid4

class ExerciseAgent(BaseAgent):
    """Agent spécialisé dans la création d'exercices personnalisés"""
    def __init__(self, llm: BaseLLMProvider[TMessage, TResponse], memory: BaseMemoryStrategy) -> None:
        super().__init__(llm, memory)

    def _build_system_prompt(self, user: User) -> Message:
        native = user.native_language.value
        target = user.target_language.value
        level = user.current_level.value

        prompt_content = (
            f"Tu es un générateur d'exercices expert en {target} pour un élève de niveau {level} "
            f"(langue maternelle : {native}).\n"
            
            "RÈGLES D'ACTION :\n"
            "1. ANALYSE DU CONTEXTE : Examine l'historique de conversation et le résumé de conversation (contexte) qui précède le dernier message utilisateur. "
            "Identifie les concepts grammaticaux ou le principaux thèmes qui ont été enseigné.\n"
            
            "2. OBJECTIF : Ton unique but est de générer un exercice. Tu jugeras le nombre de question adéquat sauf demande explicite."
            "et ciblé sur ces concept, en l'adaptant strictement au niveau {level}.\n"
            
            "3. FORMAT : Propose un type d'exercice pertinent (ex: trous à compléter, traduction de phrases courtes, ou une simple question ouverte).\n"
            
            "4. TON : Reste neutre et encourageant. Ne donne PAS la réponse. Demande à l'élève de te répondre.\n"
            
            "5. SORTIE : Ta réponse NE DOIT CONTENIR QUE l'énoncé de l'exercice, sans préambule sur ton rôle ou explication."
        )

        return Message(
            conversation_id=uuid4(), # ID temporaire, le Message SYSTEM n'est pas enregistré
            role=Role.SYSTEM,
            content=prompt_content
        )