from abc import ABC, abstractmethod
from typing import Any, Dict, List
import json

from src.models.model import User, Message
from src.core.enums import Role
from src.services.llm.azure_llm_services import AzureFoundryLLM

from src.utils.logger import get_logger
from src.utils.prompts import CONVERSATIONAL_PROMPT, GRAMMAR_PROMPT, ROUTER_PROMPT
from src.utils.fixtures import sample_user_french_to_english, sample_conversation_history

logger = get_logger(__name__)

class BaseAgent(ABC):
    """Classe abstraite des agents"""
    def __init__(self, llm: AzureFoundryLLM):
        self.llm = llm

    @abstractmethod
    def run(self, message: Dict[str, str], user: User, conversation_history: List[Message]) -> Any:
        """
        Fonction principale executant le rôle de l'agent
        Args: 
            - message: Message de l'utilisateur
            - user: Informations de l'utilisateur
            - conversation_history: Historique de la conversation
        """
        pass

    @abstractmethod
    def _build_prompt(self, user: User) -> str:
        pass

class ConversationalAgent(BaseAgent):
    """(Temporaire) Agent par défaut qui discute avec l'utilisateur de n'importe quel topic sans demande spécifique"""
    def __init__(self, llm: AzureFoundryLLM):
        super().__init__(llm=llm)
        
    def run(self, message: Dict[str, str], user: User, conversation_history: List[Message]) -> Any:
        system_prompt = self._build_prompt(user)
        messages = self._format_history_for_llm(conversation_history)
        
        messages.append(message)
        
        try:
            response = self.llm.generate(messages, system_prompt)
            logger.info(f"Le LLM a bien généré la réponse pour {user.name}")
            return response
        except Exception as e:
            logger.error(f"Une erreur est survenue pendant la génération de la réponse pour {user.name}: {e}")
            return "Veuillez réessayer."
    
    def _build_prompt(self, user: User) -> str:
        return CONVERSATIONAL_PROMPT.format(name=user.name, level=user.current_level)

    def _format_history_for_llm(self, conversation_history: List[Message]) -> List[Dict[str, str]]:
        return [
            {"role": message.role.value, "content": message.content} 
            for message in conversation_history
            if message.role != Role.SYSTEM
        ]


class GrammarAgent(BaseAgent):
    """
    Cet agent permet de corriger les erreurs de grammaire faites par l'utilisateur. 
    Utilisé lorsque l'utilisateur demande explicitement des corrections, ou lors du recap de la conversation.
    """
    def __init__(self, llm: AzureFoundryLLM):
        super().__init__(llm=llm)

        
    def run(self, message: Dict[str, str], user: User, conversation_history: List[Message]) -> Any:
        system_prompt = self._build_prompt(user)
        
        try:
            response = self.llm.generate([message], system_prompt)
            logger.info(f"Le LLM a bien généré la réponse pour {user.name}")
            return response
        except Exception as e:
            logger.error(f"Une erreur est survenue pendant la génération de la réponse pour {user.name}: {e}")
            return "Veuillez réessayer."
    
    def _build_prompt(self, user: User) -> str:
        return GRAMMAR_PROMPT.format(name=user.name)
    

class RouterAgent(BaseAgent):
    """Agent orchestrateur, appelle les différents agents en leur passant les outils nécessaires selon les requêtes de l'utilisateur"""
    def __init__(self, llm: AzureFoundryLLM):
        super().__init__(llm)
        
        self.conversational = ConversationalAgent(self.llm)
        self.grammar = GrammarAgent(self.llm)
        
        self.tool_mapping = {
            "call_conversational_agent": self.conversational.run,
            "call_grammar_agent": self.grammar.run,
        }


    def run(self, message: Dict[str, str], user: User, conversation_history: List[Message]) -> str:
        prompt = self._build_prompt(user)
        response = self.llm.generate_tool_call(messages=[message], tools=self._get_schema_tools(user), system_prompt=prompt)
        
        res = ""
        for tool in response:
            if tool.type == "function":
                function_name = tool.function.name
                args = json.loads(tool.function.arguments)
                
                call_func = self.tool_mapping.get(function_name)

                if call_func is None:
                    logger.warning(f"Le tool {function_name} n'existe pas. Utilisation de l'agent conversationnel par défaut.")
                    call_func = self.tool_mapping["call_conversational_agent"]
                
                message_for_agent: Dict[str, str] = {"role": "user", "content": args["user_message"]}
                # Pas d'utilisation de la mémoire pour l'instant
                res = call_func(message=message_for_agent, user=user, conversation_history=[])

        return res

    def _build_prompt(self, user: User) -> str:
        return ROUTER_PROMPT.format(name=user.name, tools=self._get_schema_tools(user))

    def _get_schema_tools(self, user: User) -> List[Dict[str, Any]]:
        return [
            {
                "type": "function",  
                "function": {          
                    "name": "call_grammar_agent",
                    "description": (
                        "Utilise cet outil UNIQUEMENT pour les demandes explicites de correction grammaticale, conjugaison, ou vérification de syntaxe."
                    ),
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "user_message": {
                                "type": "string",
                                "description": (
                                    "Le message exact de l'utilisateur à corriger."
                                )
                            }
                        },
                    },
                    "required": ["user_message"],
                } ,
            },
            {
                "type": "function",
                "function": {
                    "name": "call_conversational_agent",
                    "description": (
                        "Utilise cet outil pour des conversations basiques avec l'utilisateur, sans demande de correction ou autre."
                    ),
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "user_message": {
                                "type": "string",
                                "description": "Le message envoyé par l'utilisateur."
                            }
                        }, 
                        "required": ["user_message"],
                    }
                }
            }
        ]


def main():
    """Test des agents avec des fixtures"""
    print("Test de l'orchestration ...")

    llm = AzureFoundryLLM()
    agent = RouterAgent(llm)

    user = sample_user_french_to_english
    conversation_history = sample_conversation_history
    
    message_str = "I go cinema yesterday"
    message1 = {"role": "user", "content": message_str}
    print(message_str)

    response1 = agent.run(message1, user, conversation_history)
    print(f"Agent response:\n{response1}")
    print()
        
    # message_str = "Hello teacher, today we're starting a new lesson. I want to practice my english to become fluent. " \
    # "What would you recommand me to practice first? Je veux aussi que tu me dises si j'ai fait des fautes dans les phrases."
    # message2 = {"role": "user", "content": message_str}
    # print(message_str)

    # response2 = agent.run(message2, user, conversation_history)
    # print("Agent response \n")
    # print(response2)


    # message_str = "I go cinema yesterday."
    # message3 = {"role": "user", "content": message_str}
    # print(message_str)

    # response3 = agent.run(message3, user, conversation_history)
    # print("Agent response \n")
    # print(response3)

if __name__ == "__main__":
    main()