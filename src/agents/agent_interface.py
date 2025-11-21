
from abc import ABC, abstractmethod
from src.models.user_model import User
from src.models.conversation_model import Message

from src.services.llm.providers.provider_interface import BaseLLMProvider
from src.services.memory.strategies.strategy_interface import BaseMemoryStrategy

from src.core.types import TMessage, TResponse

class BaseAgent(ABC):
    """
    Interface générique pour les différents agents
    """

    def __init__(self, llm: BaseLLMProvider[TMessage, TResponse], memory: BaseMemoryStrategy) -> None:
        self.llm=llm
        self.memory=memory

    def run(self, user_message: Message) -> Message:
        cid = user_message.conversation_id
        repo = self.memory.repository

        conversation = repo.get_conversation_by_id(cid) 
        user = repo.get_user(conversation.user_id) 
        
        self.memory.save_message(user_message)
        system_msg = self._build_system_prompt(user)
        history_context = self.memory.get_context(cid)
        
        full_context = [system_msg] + history_context + [user_message]
        
        agent_response = self.llm.generate(full_context)
        self.memory.save_message(agent_response)

        return agent_response

    @abstractmethod
    def _build_system_prompt(self, user: User) -> Message:
        pass