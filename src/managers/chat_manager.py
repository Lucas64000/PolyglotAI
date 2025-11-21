
from src.agents.agent_interface import BaseAgent
from typing import Dict
from src.models.conversation_model import Message
from src.services.memory.repositories.json_repository import JsonFileMemoryRepository
from src.core.enums import Intent, Role

from src.utils.logger import get_logger

from src.utils.fixtures import sample_user_french_to_english

logger = get_logger(__name__)

class ChatManager:
    def __init__(self, agents: Dict[str, BaseAgent], default_agent_name: str = "tutor") -> None:
        self.agents = agents
        self.default_agent_name=default_agent_name

    def _analyze_intent(self, message_str: str) -> Intent:
        if "exercise" in message_str:
            return Intent.EXERCISE
        
        return Intent.TUTOR

    def process_message(self, user_message: Message) -> Message:
        intent = self._analyze_intent(message_str=user_message.content)
        agent_name = intent.value

        target_agent = self.agents.get(agent_name)
        
        if not target_agent:
            logger.warning(f"Agent '{agent_name}' introuvable, utilisation de l'agent par défaut.")
            target_agent = self.agents[self.default_agent_name]

        logger.info(f"Routing du message vers : {agent_name.upper()}")

        response = target_agent.run(user_message)
        
        return response

def main():
    from src.factories.agent_factory import AgentFactory
    user = sample_user_french_to_english
    uid = user.id

    repo = JsonFileMemoryRepository()
    repo.create_user(user)
    conv = repo.create_conversation(uid)
    cid = conv.id

    chatbot = AgentFactory.create_chat_manager(repo=repo)

    print("=" * 60)
    print("Bienvenue dans PolyglotAI ! Tapez 'quit' pour quitter.")
    print(f"Utilisateur: {user.name} ({user.native_language.value} | {user.target_language.value})")
    print("=" * 60)

    while True:
        try:
            user_input = input("Vous: ").strip()
            if user_input.lower() in ['quit', 'exit', 'q']:
                # Si la conversation est vide lors de la déconnexion on la supprime
                if len(repo.get_messages(cid)) == 0:
                    repo.delete_conversation(cid)
                break
            
            if not user_input:
                continue

            user_message = Message(
                conversation_id=cid,
                role=Role.USER,
                content=user_input
            )
            
            agent_response = chatbot.process_message(user_message)
            
            print(f"\nAssistant: {agent_response.content}\n")
            
        except KeyboardInterrupt:
            # Si la conversation est vide lors de la déconnexion on la supprime
            if len(repo.get_messages(cid)) == 0:
                repo.delete_conversation(cid)
            break
        except Exception as e:
            print(f"Erreur: {e}")
            logger.error(f"Erreur dans le main: {e}")

if __name__ == "__main__":
    main()