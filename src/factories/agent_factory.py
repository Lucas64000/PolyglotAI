
from typing import Dict

from .llm_factory import LLMFactory

from src.services.memory.repositories.repository_interface import BaseMemoryRepository
from src.services.memory.repositories.json_repository import JsonFileMemoryRepository
from src.services.memory.strategies.window_strategy import WindowMemoryStrategy
from src.services.memory.strategies.summary_strategy import SummaryMemoryStrategy

from src.agents.agent_interface import BaseAgent
from src.agents.tutor_agent import TutorAgent
from src.agents.exercise_agent import ExerciseAgent

from src.managers.chat_manager import ChatManager

from src.utils.config import get_config

class AgentFactory:
    """
    L'Assembleur Unique. 
    Il construit tout ce qui est nécessaire pour lancer l'application.
    """

    @staticmethod
    def create_chat_manager(provider_name: str | None = None, model_name: str | None = None, temperature: float | None = None, repo: BaseMemoryRepository = JsonFileMemoryRepository()) -> ChatManager:
        config = get_config()
        
        provider = provider_name if provider_name is not None else config.provider_default
        model = model_name if model_name is not None else config.model_name_default
        temp = temperature if temperature is not None else config.temperature_default

        llm = LLMFactory.create_llm_provider(
            provider_name=provider,
            model_name=model,
            temperature=temp
        )

        repo = repo
        # On suppose ces strategies pour démontrer l'utilisation de différentes stratégies pour chaque agent
        window_memory = WindowMemoryStrategy(repository=repo, window_size=10)
        summary_memory = SummaryMemoryStrategy(repository=repo, llm=llm)

        tutor = TutorAgent(llm=llm, memory=window_memory)        # Le tuteur a besoin des derniers messages uniquement
        exercise = ExerciseAgent(llm=llm, memory=summary_memory) # Pour les exercices on a besoin d'un résumé sur les notions vues

        agents_map: Dict[str, BaseAgent] = {
            "tutor": tutor,
            "exercise": exercise
        }
        
        return ChatManager(agents=agents_map, default_agent_name="tutor")