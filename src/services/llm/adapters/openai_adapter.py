
from typing import List, cast
from datetime import datetime, timezone
from uuid import UUID

from openai.types.chat import ChatCompletion, ChatCompletionMessageParam
from src.models.conversation_model import Message
from src.core.enums import Role

from .adapter_interface import MessageAdapter

class OpenAIMessageAdapter(MessageAdapter[ChatCompletionMessageParam, ChatCompletion]):
    """
    Adapter pour convertir les Messages métier vers le format OpenAI (ChatCompletionMessageParam)
    et convertir la réponse OpenAI (ChatCompletion) vers un Message métier.
    """

    def to_sdk_format(self, messages: List[Message]) -> List[ChatCompletionMessageParam]:
        """
        Convertit une liste de Messages métier en messages format SDK OpenAI

        Args:
            messages (List[Message]): Liste de Messages métier avec rôle et contenu

        Returns:
            List[ChatCompletionMessageParam]: Liste de messages compatible avec l'API OpenAI
        """
        return [
            # msg.role.value: Literal["user", "assistant", "system"], type safe
            cast(ChatCompletionMessageParam, {"role": msg.role.value, "content": msg.content})
            for msg in messages 
        ]

    def from_sdk_response(self, response: ChatCompletion, conversation_id: UUID) -> Message:
        """
        Convertit une réponse OpenAI (ChatCompletion) en Message métier

        Args:
            response (ChatCompletion): Objet renvoyé par le SDK OpenAI
            conversation_id (UUID): L'ID de la conversation associée

        Returns:
            Message: Message métier avec rôle ASSISTANT, contenu de la réponse et metadata 
        """
        created_dt = datetime.fromtimestamp(response.created, tz=timezone.utc)
        
        return Message(
            conversation_id=conversation_id,
            role=Role.ASSISTANT,
            content=response.choices[0].message.content or "",
            metadata={
                "api_response_id": response.id,
                "api_created_at": created_dt.isoformat(),  
                "usage": response.usage.model_dump() if response.usage else None
            }
        )


