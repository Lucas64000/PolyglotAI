
from typing import List, Dict, Any
import json
from src.models.conversation_model import Message
from openai.types.chat import ChatCompletion, ChatCompletionMessageParam

from .provider_interface import BaseLLMProvider
from src.clients.client_interface import ClientWrapper
from src.adapters.llm_adapter.adapter_interface import MessageAdapter

from src.core.exceptions.llm_exceptions import LLMError, LLMJSONDecodeError, LLMResponseError
from src.utils.logger import get_logger

logger = get_logger(__name__)

class AzureLLMProvider(BaseLLMProvider[ChatCompletionMessageParam, ChatCompletion]):
    """
    Implémentation du provider métier LLM pour Azure.
    Encapsule la logique de génération de texte et la conversion des messages via l'adapter OpenAIMessageAdapter
    """

    def __init__(
        self,
        model_name: str,
        temperature: float,
        max_tokens: int,
        client: ClientWrapper[ChatCompletionMessageParam, ChatCompletion],
        adapter: MessageAdapter[ChatCompletionMessageParam, ChatCompletion]
    ):
        """
        Initialise le provider Azure LLM avec les composants injectés

        Args:
            model_name: Nom du deployment Azure
            temperature: Température de génération
            max_tokens: Nombre maximum de tokens
            client: Client wrapper Azure OpenAI déjà configuré
            adapter: Adaptateur de messages OpenAI
        """
        super().__init__(model_name, temperature, max_tokens, client, adapter)


    def generate(self, messages: List[Message]) -> Message:
        """
        Génère un message métier à partir de messages métier (historique de conversation)

        Args:
            messages: Liste de messages métier de la conversation

        Returns:
            Message métier contenant la réponse du LLM

        Raises:
            LLMError: Erreur lors de l'appel à l'API
            LLMResponseError: Réponse vide ou invalide du LLM
        """
        sdk_messages = self.adapter.to_sdk_format(messages)
        
        try:
            response: ChatCompletion = self.client.generate(
                messages=sdk_messages,
                model_name=self.model_name,
                max_tokens=self.max_tokens,
                temperature=self.temperature,
            )
            logger.info(f"Appel LLM réussi pour le modèle {self.model_name}.")

        except Exception as e:
            logger.error(f"Erreur Azure : {e}")
            raise LLMError(f"Échec de l'appel LLM : {e}") from e

        if not response.choices or not response.choices[0].message.content:
            raise LLMResponseError("Réponse vide du LLM")

        conversation_id=messages[0].conversation_id
        return self.adapter.from_sdk_response(response, conversation_id)

    def generate_json(self, messages: List[Message]) -> Dict[str, Any]:
        """
        Génère une réponse JSON à partir de messages métier

        Args:
            messages: Liste de messages métier

        Returns:
            Contenu JSON de la réponse du LLM

        Raises:
            LLMError: Erreur API
            LLMResponseError: Réponse vide
            LLMJSONDecodeError: JSON invalide
        """
        sdk_messages = self.adapter.to_sdk_format(messages)

        try:
            response: ChatCompletion = self.client.generate_json(
                messages=sdk_messages,
                model_name=self.model_name,
                max_tokens=self.max_tokens,
                temperature=self.temperature,
            )
            logger.info(f"Appel LLM JSON réussi ({self.model_name})")

        except Exception as e:
            logger.error(f"Erreur Azure : {e}")
            raise LLMError(f"Échec de l'appel LLM : {e}") from e

        if not response.choices or not response.choices[0].message.content:
            raise LLMResponseError("Réponse vide du LLM")

        content = response.choices[0].message.content

        try:
            return json.loads(content)
        except json.JSONDecodeError as e:
            logger.error("JSON invalide")
            raise LLMJSONDecodeError(f"JSON invalide : {e}") from e


#     # A revoir pour plus tard

#     # def generate_tool_calls(
#     #         self, 
#     #         messages: List[Message], 
#     #         tools: List[Dict[str, Any]], 
#     #         temperature: float = 0.0    
#     #     ) -> Any:
#     #     """
#     #     Génère une réponse incluant un appel d'outil.
        
#     #     Args:
#     #         messages: Liste des messages de la conversation.
#     #         tools: Définitions des fonctions disponibles pour le modèle.
#     #         temperature: Température de génération. (0.0 par défaut pour le routage).
            
#     #     Returns:
#     #         La liste des tools à utiliser
#     #     """
#     #     typed_messages = cast(List[ChatCompletionMessageParam], messages)
#     #     typed_tools = cast(List[ChatCompletionToolParam], tools)

#     #     try:
#     #         response: ChatCompletion = self.client.chat.completions.create(
#     #             messages=typed_messages,
#     #             model=self.model_name,
#     #             temperature=temperature,
#     #             max_tokens=self.max_tokens,
#     #             tools=typed_tools, 
#     #         )
            
#     #         logger.info(f"Appel LLM (Tool Call) réussi pour le modèle {self.model_name}.")

#     #         if not response.choices:
#     #             logger.warning("La réponse de l'API est vide (pas de 'choices').")
#     #             return None
            
#     #         return response.choices[0].message.tool_calls
            
#     #     except Exception as e:
#     #         logger.error(f"Erreur lors de l'appel à Azure/generate_tool_call : {e}")
#     #         return None 