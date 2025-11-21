
from typing import List

from uuid import UUID
from src.models.conversation_model import Message
from src.core.enums import Role
from src.services.memory.repositories.repository_interface import BaseMemoryRepository
from src.services.memory.strategies.strategy_interface import BaseMemoryStrategy
from src.services.llm.providers.provider_interface import BaseLLMProvider 
from src.utils.logger import get_logger

from src.core.types import TMessage, TResponse

logger = get_logger(__name__)

class SummaryMemoryStrategy(BaseMemoryStrategy):

    def __init__(
        self, 
        repository: BaseMemoryRepository, 
        llm: BaseLLMProvider[TMessage, TResponse], 
        window_size: int = 5,
        summary_threshold: int = 10 
    ) -> None:
        super().__init__(repository)
        self.llm = llm
        self.window_size = window_size
        self.summary_threshold = summary_threshold

    def get_context(self, cid: UUID) -> List[Message]:
        """
        Construit le contexte hybride : [Résumé] + [Messages Récents]
        """
        conversation = self.repository.get_conversation_by_id(cid)
        current_summary = conversation.summary 

        context_list: List[Message] = []

        if current_summary:
            summary_msg = Message(
                conversation_id=cid,
                role=Role.SYSTEM,
                content=f"RÉSUMÉ DU CONTEXTE PRÉCÉDENT :\n{current_summary}"
            )
            context_list.append(summary_msg)

        all_messages = self.repository.get_messages(cid)
        recent_messages = all_messages[-self.window_size:]
        
        context_list.extend(recent_messages)

        return context_list

    def save_message(self, message: Message) -> None:
        """
        Sauvegarde le message et déclenche une condensation si l'historique est trop long.
        """
        cid = message.conversation_id
        
        self.repository.save_message(message)

        all_messages = self.repository.get_messages(cid)
        
        # Déclenche le résumé tous les self.summary_threshold + self.window_size messages
        if len(all_messages) >= (self.summary_threshold + self.window_size) and len(all_messages) % (self.summary_threshold + self.window_size) == 0:
            self._condense_history(cid, all_messages)

    def _condense_history(self, cid: UUID, all_messages: List[Message]):
        """
        Logique interne pour appeler le LLM et mettre à jour le résumé.
        """
        logger.info(f"Déclenchement du résumé pour la conversation {cid}")

        messages_to_summarize = all_messages[:-self.window_size]
        
        conversation = self.repository.get_conversation_by_id(cid)
        old_summary = conversation.summary 

        summary_prompt = (
            "Tu es un expert en synthèse. Ton but est de mettre à jour le résumé d'une conversation.\n"
            f"ANCIEN RÉSUMÉ : {old_summary}\n\n"
            "NOUVEAUX MESSAGES À INTÉGRER :\n"
        )
        
        for msg in messages_to_summarize:
            summary_prompt += f"{msg.role.value}: {msg.content}\n"
            
        summary_prompt += "\nINSTRUCTION : Génère un nouveau résumé concis qui combine l'ancien résumé et les nouvelles informations importantes."

        prompt_msg = Message(conversation_id=cid, role=Role.USER, content=summary_prompt)

        try:
            response = self.llm.generate([prompt_msg])
            new_summary = response.content

            conversation.summary = new_summary
            self.repository.update_conversation_metadata(conversation)
            
            logger.info("Résumé mis à jour avec succès.")

        except Exception as e:
            logger.error(f"Échec de la génération du résumé : {e}")