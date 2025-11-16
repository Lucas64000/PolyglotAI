from src.models.user_model import User
from src.models.conversation_model import Message
from src.core.enums import Role

from src.services.providers.provider_llm import ProviderLLM
from src.services.memory.memory_service import MemoryService
from .base_agent import BaseAgent

from src.utils.logger import get_logger
from src.utils.prompts import CONVERSATIONAL_PROMPT

from src.exceptions.llm_exceptions import LLMError, LLMResponseError

logger = get_logger(__name__)

class ConversationalAgent(BaseAgent):
    def __init__(self, llm: ProviderLLM, memory: MemoryService):
        super().__init__(llm, memory)

    def run(self, user: User, message: Message) -> Message:
        messages = self.format_messages(user, message)
        
        try:
            response = self.llm.generate(messages)
            
            self.memory.save_message(message) 
            self.memory.save_message(response) 
            
            return response
            
        except (LLMError, LLMResponseError) as e:
            logger.error(f"Erreur de génération du LLM pour {user.name} (Type: {e.__class__.__name__}): {e}")
            
            return Message(
                role=Role.ASSISTANT, 
                content="Je suis désolé, une erreur dûe au LLM est survenue."
            )
        except Exception as e:
            # A implémenter plus tard, avec des erreurs spécifiques
            logger.error(f"Erreur inattendue dans l'agent pour {user.name}: {e}")
            return Message(
                role=Role.ASSISTANT, 
                content="Une erreur inconnue s'est produite."
            )
    
    def _build_prompt(self, user: User) -> Message:
        return Message(
            role = Role.SYSTEM, 
            content = CONVERSATIONAL_PROMPT.format(user=user)
        )
    

