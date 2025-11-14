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
            return response
        except Exception as e:
            logger.error(f"Une erreur est survenue pendant la génération de la réponse pour {user.name}: {e}")
            return "Veuillez réessayer."
    
    def _build_prompt(self, user: User) -> str:
        return CONVERSATIONAL_PROMPT.format(user=user)

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
            response = self.llm.generate([message], system_prompt, temperature=0.0)
            return response
        except Exception as e:
            logger.error(f"Une erreur est survenue pendant la génération de la réponse pour {user.name}: {e}")
            return "Veuillez réessayer."
    
    def _build_prompt(self, user: User) -> str:
        return GRAMMAR_PROMPT.format(user=user)
    

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
        tool_calls = self.llm.generate_tool_call(messages=[message], tools=self._get_schema_tools(user), system_prompt=prompt, temperature=0.0)
        
        if not tool_calls:
            logger.info("Le router n'a pas choisi de tools.")
            return "Veuillez réessayer"

        tool_responses: List[Any] = [] 

        for tool_call in tool_calls:
            function_name = tool_call.function.name
            
            try:
                args_data = json.loads(tool_call.function.arguments)
                
                content = self._extract_content_for_agent(function_name, args_data)

                agent_run_method = self.tool_mapping.get(function_name)
                
                if agent_run_method and content is not None:
                    message_for_agent = {"role": "user", "content": content}
                    logger.info(f"Tool utilisé: {function_name} avec comme message: {content}")
                    
                    agent_result = agent_run_method(message_for_agent, user, [])
                    
                    tool_responses.append({
                        "agent": function_name,
                        "result": agent_result
                    })
                else:
                    logger.error(f"L'execution du tool {function_name} a échoué: Agent non trouvé ou contenu manquant.")
                    
            except json.JSONDecodeError as e:
                logger.error(f"Erreur lors du chargement des arguments au format JSON {function_name}: {e}")
            except Exception as e:
                logger.error(f"Erreur durant l'execution de l'agent pour la fonction {function_name}: {e}")

        return self._format_final_response(tool_responses)


    def _extract_content_for_agent(self, function_name: str, args_data: Dict[str, Any]) -> str | None:
        """Extrait le contenu du message pour l'agent cible."""
        
        if function_name == "call_grammar_agent":
            return args_data.get('text_to_analyze')
        elif function_name == "call_conversational_agent":
            return args_data.get('user_message')
        
        return None

    def _format_final_response(self, results: List[Dict[str, Any]]) -> str:
        """Fusionne les résultats de tous les agents pour l'utilisateur."""
        
        if not results:
            return "Aucun agent n'a pu répondre suite à l'exécution des outils."
            
        if len(results) == 1:
            return results[0]['result']
            
        final_text = "Voici ma réponse complète :\n\n"
        for item in results:
            agent_name = item['agent'].replace('call_', '').replace('_agent', '').capitalize()
            final_text += f"--- {agent_name} Response ---\n"
            final_text += item['result'] + "\n\n"
            
        return final_text.strip()

    def _build_prompt(self, user: User) -> str:
        return ROUTER_PROMPT.format(user=user, tools=self._get_schema_tools(user))

    def _get_schema_tools(self, user: User) -> List[Dict[str, Any]]:
        return [
            {
                "type": "function",  
                "function": {          
                    "name": "call_grammar_agent",
                    "description": (
                        "Utilise cet outil UNIQUEMENT pour les demandes explicites de correction grammaticale, conjugaison, ou vérification de syntaxe. "
                        "**La demande de correction DOIT prévaloir sur toute intention conversationnelle.** "
                        "Ne jamais l'utiliser pour répondre à une question ouverte."
                    ),
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "text_to_analyze": {
                                "type": "string",
                                "description": (
                                "**EXTRAIS la ou les phrases à corriger.** Si l'utilisateur demande une correction, tu dois uniquement extraire le texte à corriger, pas la requête en elle même. Par exemple, si le message est 'I go cinema. Corrige si j'ai fait des fautes', tu extrais 'I go cinema'."
                                "Fais bien attention au contexte de la requête, l'utilisateur peut très bien demander de corriger en {user.native_language.value}, alors qu'il parle des fautes en {user.target_language.value}. "
                                "Dans ce là, tu dois porter ton attention sur le message {user.target_language.value} et pas sur le message {user.native_language.value}."
                                )
                            }
                        },
                    },
                    "required": ["text_to_analyze"],
                } ,
            },
            {
                "type": "function",
                "function": {
                    "name": "call_conversational_agent",
                    "description": (
                        "Utilise cet outil pour TOUTES les conversations générales, déclarations, salutations, questions ouvertes, ou comme agent par DÉFAUT lorsque l'intention n'est pas une demande explicite de correction."
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
        
    message_str = "Hello teacher, today we're starting a new lesson. I want to practice my english to become fluent. " \
    "What would you recommand me to practice first? Corrige les fautes s'il y en a."
    # Fautes attendues: recommand me to practice
    message1 = {"role": "user", "content": message_str}
    print(message_str)
    print()

    response1 = agent.run(message1, user, conversation_history)
    print(response1)
    print()

    print("="*60)
    print()

    message_str = "I go cinema yesterday."
    message2 = {"role": "user", "content": message_str}
    print(message_str)
    print()

    response2 = agent.run(message2, user, conversation_history)
    print(response2)
    print()

if __name__ == "__main__":
    main()