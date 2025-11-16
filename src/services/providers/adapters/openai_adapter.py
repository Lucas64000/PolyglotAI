"""
Adapter pour convertir les messages au format OpenAI/Azure
"""

from typing import List, cast
from datetime import datetime, timezone

from openai.types.chat import ChatCompletion, ChatCompletionMessageParam

from src.models.conversation_model import Message
from src.core.enums import Role


class OpenAIAdapter:

    @staticmethod
    def to_provider_format(
        messages: List[Message]
    ) -> List[ChatCompletionMessageParam]:
        """Convertit Message métier en ChatCompletionMessageParam"""
        
        provider_messages: List[ChatCompletionMessageParam] = []
        
        for msg in messages:
            provider_msg = cast(ChatCompletionMessageParam, {
                "role": msg.role.value,     # msg.role.value: Literal["user", "assistant", "system"], type safe
                "content": msg.content
            })
            
            provider_messages.append(provider_msg)
        
        return provider_messages

    @staticmethod
    def from_provider_response(response: ChatCompletion) -> Message:
        """
        Convertit ChatCompletionMessageParam en Message métier
        
        Args:
            response: Message au format OpenAI
            conversation_id: ID de la conversation
            user_id: ID de l'utilisateur
            
        Returns:
            Liste de Message avec métadonnées 
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
