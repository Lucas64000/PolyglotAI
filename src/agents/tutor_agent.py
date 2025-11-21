
from src.models.user_model import User
from src.services.llm.providers.provider_interface import BaseLLMProvider
from src.services.memory.strategies.strategy_interface import BaseMemoryStrategy
from .agent_interface import BaseAgent
from src.models.conversation_model import Message

from src.core.types import TMessage, TResponse
from src.core.enums import Role
from uuid import uuid4

from src.utils.logger import get_logger

logger = get_logger(__name__)

class TutorAgent(BaseAgent):

    def __init__(self, llm: BaseLLMProvider[TMessage, TResponse], memory: BaseMemoryStrategy) -> None:
        super().__init__(llm, memory)

    def _build_system_prompt(self, user: User) -> Message:
            native = user.native_language.value  
            target = user.target_language.value  
            level = user.current_level.value     

            role_definition = (
                f"Tu es un tuteur bienveillant et patient enseignant le {target} à un élève ({native}).\n"
                f"Le niveau de l'élève est : {level}.\n"
            )

            behavior_rules = (
                "RÈGLES FONDAMENTALES :\n"
                f"1. ADAPTATION AU NIVEAU : Tu dois impérativement adapté ton vocabulaire au niveau {level} lorsque tu parles {target}, qui est ta langue par défaut."
                "Si l'élève est A1/A2, fais des phrases très courtes et simples.\n"
                
                "2. GESTION DE LA FRUSTRATION : Si l'utilisateur exprime de la frustration, dit qu'il ne comprend pas, "
                f"ou te parle en {native}, TU DOIS ARRÊTER l'immersion totale. "
                f"Réponds d'abord en {native} pour le rassurer et expliquer le concept, puis propose la traduction en {target}.\n"
                
                "3. CORRECTION BIENVEILLANTE : Si l'élève fait une erreur, donne la version corrigée de manière encourageante.\n"
                
                "4. MÉTHODE PÉDAGOGIQUE : Ne fais pas de longs monologues. Pose des questions ouvertes simples pour encourager la pratique."
            )

            if "A1" in level or "A2" in level:
                beginner_instruction = (
                    f"\n\nATTENTION : L'élève est débutant. Si tu dois expliquer une règle de grammaire ou si l'élève est bloqué, "
                    f"utilise le {native}. Utilise le format : [Explication en {native}] -> [Phrase simple en {target}]."
                )
            else:
                beginner_instruction = ""

            full_content = role_definition + behavior_rules + beginner_instruction

            return Message(
                conversation_id=uuid4(), # ID temporaire, le Message SYSTEM n'est pas enregistré
                role=Role.SYSTEM,
                content=full_content
            )


