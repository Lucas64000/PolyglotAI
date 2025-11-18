
from typing import List, cast
from datetime import datetime, timezone

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
        Convertit une liste de Messages métier en messages format SDK OpenAI.

        Args:
            messages (List[Message]): Liste de Messages métier avec rôle et contenu.

        Returns:
            List[ChatCompletionMessageParam]: Liste de messages compatible avec l'API OpenAI.
        """
        return [
            # msg.role.value: Literal["user", "assistant", "system"], type safe
            cast(ChatCompletionMessageParam, {"role": msg.role.value, "content": msg.content})
            for msg in messages
        ]

    def from_sdk_response(self, response: ChatCompletion) -> Message:
        """
        Convertit une réponse OpenAI (ChatCompletion) en Message métier.

        Args:
            response (ChatCompletion): Objet renvoyé par le SDK OpenAI.

        Returns:
            Message: Message métier avec rôle ASSISTANT, contenu et metadata (id et date de création UTC).
        """
        created_dt = datetime.fromtimestamp(response.created, tz=timezone.utc)
        
        return Message(
            role=Role.ASSISTANT,
            content=response.choices[0].message.content or "",
            metadata={
                "id": response.id,
                "created_at": created_dt.isoformat(),  
            }
        )


