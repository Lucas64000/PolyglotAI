"""
All conversations-related Use Case

Orchestrates the creation of a conversation and sending messages within a conversation.
"""

from uuid import uuid4

from src.core.ports import ChatProvider, ConversationRepository, TimeProvider
from src.core.domain import (
    # Value objects
    Role, 
    TeacherProfile, 
    CreativityLevel, 
    GenerationStyle,
    # Entities
    Conversation,
)
from src.core.exceptions import ResourceNotFoundError

from src.application.dtos.conversations import (
    # CreateConversationUseCase
    CreateConversationCommand, CreateConversationResult,
    # SendMessageUsecase
    SendMessageCommand, SendMessageResult,
    # DeleteConversationUseCase
    DeleteConversationCommand,
)

class CreateConversationUseCase:
    """
    Application use case for creating a learning conversation.
    
    This use case coordinates:
    1. Creating a conversation for the student
    2. Persisting the new conversation
    """

    def __init__(
        self,
        repository: ConversationRepository,
        time_provider: TimeProvider,
    ) -> None:
        """
        Initialize the use case with required dependencies.
        
        Args:
            repository: Repository for conversation persistence
            time_provider: Port for retrieving current time
        """
        self._repository = repository
        self._time_provider = time_provider

    async def execute(self, command_dto: CreateConversationCommand) -> CreateConversationResult:
        """
        Execute the create conversation use case.
        
        Workflow:
        1. Create the Conversation entity
        2. Persist conversation

        Args:
            command_dto: Command containing student ID and conversation settings
            
        Returns:
            Result containing conversation ID

        Raises:
            ResourceAlreadyExistsError: If the conversation already exists in the repository
            InvalidLanguagePairError: If native_lang and target_land are identic
            PersistenceError: If repository fails to persist conversation
        """
        # Generate ID and timestamps for the conversation
        conversation_id = uuid4()
        now = self._time_provider.now()

        conversation_title = command_dto.title if command_dto.title and command_dto.title.strip() else "New Conversation"
        
        # 1. Create the Conversation entity
        conversation = Conversation.create_new(
            id=conversation_id,
            student_id=command_dto.student_id,
            title=conversation_title,
            native_lang=command_dto.native_lang,
            target_lang=command_dto.target_lang,
            now=now,
        )

        # 2. Persist conversation
        await self._repository.save(conversation=conversation)

        # Return the result with conversation ID
        return CreateConversationResult(
            conversation_id=conversation_id
        )

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
        repository: ConversationRepository,
        time_provider: TimeProvider,
    ) -> None:
        """
        Initialize the use case with required dependencies.
        
        Args:
            chat_provider: Port for getting teacher's responses
            repository: Repository for conversation persistence
            time_provider: Port for retrieving current time
        """
        self._chat_provider = chat_provider
        self._repository = repository
        self._time_provider = time_provider

    async def execute(self, command_dto: SendMessageCommand) -> SendMessageResult:
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
            command_dto: Command containing conversation ID, student message, 
                        teacher profile params and conversation language settings
            
        Returns:
            Result containing messages IDs and teacher message 
            
        Raises:
            ResourceNotFoundError: If conversation does not exist
            ConversationNotWritableError: If conversation is archived or deleted
            TeacherGenerationError: If service fails to get teacher response
        """
        # 1. Retrieve the conversation by ID
        conversation = await self._repository.get_by_id(command_dto.conversation_id)
        
        # Generate IDs and timestamps for the student message
        student_message_id = uuid4()
        now_student = self._time_provider.now()
    
        # 2. Add the student's message to the conversation
        _ = conversation.add_message(
            new_message_id=student_message_id,
            now=now_student,
            role=Role.STUDENT,
            content=command_dto.student_message,
        )

        # Prepare the history and teacher profile for generation
        history = tuple(conversation.messages)
        teacher_profile = TeacherProfile(
            creativity_level=CreativityLevel(command_dto.creativity_level), 
            generation_style=GenerationStyle(command_dto.generation_style)
        )

        # 3. Get the teacher's response
        teacher_response = await self._chat_provider.get_teacher_response(
            history=history, 
            teacher_profile=teacher_profile,
            native_lang=conversation.native_lang,
            target_lang=conversation.target_lang,
        )

        # Generate IDs and timestamps for the teacher message
        teacher_message_id = uuid4()
        now_teacher = self._time_provider.now()
        
        # 4. Add the teacher's message to the conversation
        _ = conversation.add_message(
            new_message_id=teacher_message_id,
            now=now_teacher,
            role=Role.TEACHER,
            content=teacher_response
        )

        # 5. Save the updated conversation
        await self._repository.save(conversation)

        # 6. Return the result with message IDs and teacher message
        return SendMessageResult(
            message_id=teacher_message_id,
            student_message_id=student_message_id,
            teacher_message=teacher_response
        )
    

class DeleteConversationUseCase:
    """
    Application use case for deleting a conversation.
    
    This use case coordinates:
    1. Verifying conversation ownership (security check)
    2. Removing the conversation from persistence
    
    Security note: Returns ResourceNotFoundError for both non-existent 
    conversations and conversations owned by other users to prevent enumeration.
    """

    def __init__(
            self, 
            repository: ConversationRepository,
            time_provider: TimeProvider,
        ) -> None:
        """
        Initialize the use case with required dependencies.
        
        Args:
            repository: Repository for conversation persistence
            time_provider: Port for retrieving current time
        """
        self._repository = repository
        self._time_provider = time_provider

    async def execute(self, command: DeleteConversationCommand) -> None:
        """
        Execute the delete conversation use case.
        
        Workflow:
        1. Fetch the conversation to verify it exists
        2. Verify ownership (security check)
        3. Remove the conversation
        
        Args:
            command: Command containing conversation ID and student ID
            
        Raises:
            ResourceNotFoundError: If conversation doesn't exist OR if the requester is not the owner
        """
        # 1. Fetch the conversation to check ownership
        conversation = await self._repository.get_by_id(command.conversation_id)

        # 2. Security Check: Is the requester the owner?
        if conversation.student_id != command.student_id:
            raise ResourceNotFoundError(resource_type="Conversation", resource_id=command.conversation_id)
        
        conversation.delete(now=self._time_provider.now())

        # 3. Remove the conversation (soft delete)
        await self._repository.save(conversation=conversation)