"""Implémentation du service de LLM avec le provider Azure"""
from typing import List, Dict, Any
from src.models.conversation_model import Message
from openai.types.chat import ChatCompletion

from .provider_llm import ProviderLLM
from openai import AzureOpenAI
from .adapters.openai_adapter import OpenAIAdapter
from src.exceptions.llm_exceptions import (
    LLMError,
    LLMJSONDecodeError,
    LLMResponseError
)
import json 

from src.utils.logger import get_logger

logger = get_logger(__name__)

class AzureLLM(ProviderLLM):
    def __init__(self, api_key: str, endpoint: str, deployment_name: str, api_version: str, 
                 max_tokens: int, temperature: float) -> None:
        
        super().__init__(
            model_name=deployment_name,
            max_tokens=max_tokens,
            temperature=temperature,
        )

        self.client = AzureOpenAI(
            azure_endpoint=endpoint,
            azure_deployment=deployment_name,
            api_version=api_version,
            api_key=api_key
        )

        self.adapter = OpenAIAdapter()

    def generate(self, messages: List[Message]) -> Message:
        """
        Génère une réponse textuelle à partir d'une liste de messages.
        
        Args:
            messages: Liste des messages de la conversation.
        
        Returns:
            Le Message de la réponse du modèle.

        Raises:
            LLMError: En cas d'erreur API
            LLMResponseError: Si la réponse est invalide
        """
        openai_messages = OpenAIAdapter.to_provider_format(messages=messages)
        try:
            response: ChatCompletion = self.client.chat.completions.create(
                messages=openai_messages,
                model=self.model_name,
                max_tokens=self.max_tokens,
                temperature=self.temperature,
            )
            logger.info(f"Appel LLM réussi pour le modèle {self.model_name}.")

        except Exception as e:
            logger.error(f"Erreur Azure: {e}")
            raise LLMError(f"Échec appel LLM: {e}") from e
        
        if not response.choices or not response.choices[0].message.content:
            raise LLMResponseError("Réponse vide du LLM")
        
        return OpenAIAdapter.from_provider_response(response)

    # Implémenté mais pas forcément utile, à voir plus tard    
    def generate_json(self, messages: List[Message]) -> Dict[str, Any]:
        """
        Génère une réponse au format JSON à partir d'une liste de messages.
        
        Args:
            messages: Liste des messages de la conversation.
        
        Returns:
            Le contenu de la réponse du modèle au format Dict (représentant l'objet JSON).

        Raises:
            LLMError: En cas d'erreur API
            LLMResponseError: Si la réponse est invalide
            LLMJSONDecodeError: Si le JSON est invalide
        """
        openai_messages = OpenAIAdapter.to_provider_format(messages)
        
        try:
            response: ChatCompletion = self.client.chat.completions.create(
                messages=openai_messages,
                model=self.model_name,
                max_tokens=self.max_tokens,
                temperature=self.temperature,
                response_format={"type": "json_object"}
            )
            logger.info(f"Appel LLM JSON réussi ({self.model_name})")
            
        except Exception as e:
            logger.error(f"Erreur Azure: {e}")
            raise LLMError(f"Échec appel LLM: {e}") from e
        
        if not response.choices or not response.choices[0].message.content:
            raise LLMResponseError("Réponse vide du LLM")
        
        content = response.choices[0].message.content
        
        try:
            return json.loads(content)
        except json.JSONDecodeError as e:
            logger.error(f"JSON invalide")
            raise LLMJSONDecodeError(f"JSON invalide: {e}") from e

    # A revoir pour plus tard

    # def generate_tool_calls(
    #         self, 
    #         messages: List[Message], 
    #         tools: List[Dict[str, Any]], 
    #         temperature: float = 0.0    
    #     ) -> Any:
    #     """
    #     Génère une réponse incluant un appel d'outil.
        
    #     Args:
    #         messages: Liste des messages de la conversation.
    #         tools: Définitions des fonctions disponibles pour le modèle.
    #         temperature: Température de génération. (0.0 par défaut pour le routage).
            
    #     Returns:
    #         La liste des tools à utiliser
    #     """
    #     typed_messages = cast(List[ChatCompletionMessageParam], messages)
    #     typed_tools = cast(List[ChatCompletionToolParam], tools)

    #     try:
    #         response: ChatCompletion = self.client.chat.completions.create(
    #             messages=typed_messages,
    #             model=self.model_name,
    #             temperature=temperature,
    #             max_tokens=self.max_tokens,
    #             tools=typed_tools, 
    #         )
            
    #         logger.info(f"Appel LLM (Tool Call) réussi pour le modèle {self.model_name}.")

    #         if not response.choices:
    #             logger.warning("La réponse de l'API est vide (pas de 'choices').")
    #             return None
            
    #         return response.choices[0].message.tool_calls
            
    #     except Exception as e:
    #         logger.error(f"Erreur lors de l'appel à Azure/generate_tool_call : {e}")
    #         return None 
        