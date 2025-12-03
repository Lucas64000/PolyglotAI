"""
ProcessMessage Use Case

Handles the core flow of processing a user message in a tutoring session.
"""

from dataclasses import dataclass
from uuid import UUID

from src.core.ports.driven import ChatModel, GraphMemory
from src.core.domain.entities import ChatMessage


@dataclass
class ProcessMessageInput:
    """Input for the process message use case."""
    session_id: UUID
    user_id: UUID
    user_message: str
    conversation_history: list[ChatMessage]


@dataclass  
class ProcessMessageOutput:
    """Output from the process message use case."""
    response: ChatMessage
    extracted_vocabulary: list[str]
    detected_errors: list[str]


class ProcessMessageUseCase:
    """
    Use case for processing a user message.
    
    Single responsibility: Take user input, generate appropriate tutor response.
    Does NOT handle session management (that's ChatService's job).
    """
    
    def __init__(
        self,
        chat_model: ChatModel,
        graph_memory: GraphMemory,
    ) -> None:
        self._chat_model = chat_model
        self._graph_memory = graph_memory
    
    async def execute(self, input_data: ProcessMessageInput) -> ProcessMessageOutput:
        """
        Execute the use case.
        
        1. Retrieve learning context from graph
        2. Build prompt with context
        3. Generate response
        4. Extract vocabulary and errors (future: via extraction agent)
        5. Return structured output
        """
        from src.core.domain.entities import ChatMessage
        from src.core.domain.value_objects import Role
        
        # Get relevant learning context
        # context = await self._graph_memory.get_learning_context(
        #     user_id=input_data.user_id,
        #     current_message=input_data.user_message,
        # )
        
        # TODO: Build sophisticated prompt with context
        # TODO: Use TutorAgent instead of direct chat_model call
        
        # Generate response
        response_text = await self._chat_model.generate(
            input_data.conversation_history
        )
        
        # Create response message
        response_message = ChatMessage(
            session_id=input_data.session_id,
            role=Role.ASSISTANT,
            content=response_text,
        )
        
        # TODO: Extract vocabulary and errors from conversation
        extracted_vocabulary: list[str] = []
        detected_errors: list[str] = []
        
        return ProcessMessageOutput(
            response=response_message,
            extracted_vocabulary=extracted_vocabulary,
            detected_errors=detected_errors,
        )
