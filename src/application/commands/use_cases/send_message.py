"""
Send Message Use Case

Orchestrates the process of adding a student message and a teacher response.
This is the primary use case for interactive learning conversations.
"""

from uuid import uuid4

from src.core.ports import ChatProvider, ConversationRepository, TimeProvider
from src.core.domain import Role, TeacherProfile, CreativityLevel, GenerationStyle

from src.application.commands.dtos.send_message import SendMessageRequest, SendMessageResponse


class SendMessageUseCase:
    """
    Application use case for handling message exchanges in learning conversations.
    
    This use case coordinates:
    1. Adding the student's message to the conversation
    2. Getting the teacher response based on conversation history and teacher profile
    3. Adding the teacher's message to the conversation
    4. Persisting the updated conversation
    
    Orchestrates between domain entities and infrastructure ports.
    """

    def __init__(
        self,
        chat_provider: ChatProvider,
        conv_repo: ConversationRepository,
        time_provider: TimeProvider,
    ) -> None:
        """
        Initialize the use case with required dependencies.
        
        Args:
            chat_provider: Port for AI response generation
            conv_repo: Repository for conversation persistence
            time_provider: Port for retrieving current time
        """
        self.chat_provider = chat_provider
        self.conv_repo = conv_repo
        self.time_provider = time_provider

    async def execute(self, request_dto: SendMessageRequest) -> SendMessageResponse:
        """
        Execute the send message use case.
        
        Workflow:
        1. Retrieve the conversation entity
        2. Add student message to conversation
        3. Get teacher response using conversation history and teacher profile
        4. Add teacher message to conversation
        5. Persist updated conversation
        6. Return response with message IDs

        Args:
            request_dto: Request containing conversation ID, student message, and teacher profile params
            
        Returns:
            Response containing messages IDs and teacher message 
            
        Raises:
            ResourceNotFoundError: If conversation does not exist
            ConversationNotWritableError: If conversation is archived or deleted
            TeacherGenerationError: If service fails to get teacher response
        """
        # Retrieve the conversation by ID
        conversation = await self.conv_repo.get_by_id(request_dto.conversation_id)
        
        # Generate IDs and timestamps for the student message
        student_message_id = uuid4()
        now_student = self.time_provider.now()
    
        # Add the student's message to the conversation
        _ = conversation.add_message(
            new_message_id=student_message_id,
            now=now_student,
            role=Role.STUDENT,
            content=request_dto.student_message,
        )

        # Prepare the history and teacher profile for generation
        history = tuple(conversation.messages)
        teacher_profile = TeacherProfile(
            creativity_level=CreativityLevel(request_dto.creativity_level), 
            generation_style=GenerationStyle(request_dto.generation_style)
        )

        # Get the teacher's response
        teacher_response = await self.chat_provider.get_teacher_response(
            history=history, 
            teacher_profile=teacher_profile,
        )

        # Generate IDs and timestamps for the teacher message
        teacher_message_id = uuid4()
        now_teacher = self.time_provider.now()
        
        # Add the teacher's message to the conversation
        _ = conversation.add_message(
            new_message_id=teacher_message_id,
            now=now_teacher,
            role=Role.TEACHER,
            content=teacher_response
        )

        # Save the updated conversation
        await self.conv_repo.save(conversation)

        # Return the response with message IDs and teacher message
        return SendMessageResponse(
            message_id=teacher_message_id,
            student_message_id=student_message_id,
            teacher_message=teacher_response
        )