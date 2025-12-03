
from uuid import UUID

from src.core.ports.driven import ChatModel, GraphMemory, UserRepository
from src.core.domain.entities import ChatMessage, LearningSession


class ChatServiceImpl:
    """
    Implementation of the ChatService interface.
    
    Orchestrates the conversation flow:
    1. Receives user message
    2. Retrieves relevant context from GraphMemory
    3. Delegates to TutorAgent for response generation
    4. Extracts vocabulary/errors from conversation
    5. Updates GraphMemory with new knowledge
    
    All dependencies are injected - no direct instantiation.
    """
    
    def __init__(
        self,
        chat_model: ChatModel,
        graph_memory: GraphMemory,
        user_repository: UserRepository,
    ) -> None:
        """
        Initialize with injected dependencies.
        
        Args:
            chat_model: For generating AI responses
            graph_memory: For storing/retrieving learning data
            user_repository: For user profile management
        """
        self._chat_model = chat_model
        self._graph_memory = graph_memory
        self._user_repository = user_repository
        self._sessions: dict[UUID, LearningSession] = {}  # In-memory for now
    
    async def start_session(
        self,
        user_id: UUID,
        focus_topic: str | None = None,
    ) -> LearningSession:
        """Start a new learning session."""
        from src.core.domain.entities import LearningSession
        
        # Verify user exists
        user = await self._user_repository.get_by_id(user_id)
        if not user:
            from src.core.exceptions import EntityNotFoundError
            raise EntityNotFoundError("User", str(user_id))
        
        # Create session
        session = LearningSession(
            user_id=user_id,
            focus_topic=focus_topic,
        )
        self._sessions[session.id] = session
        
        # Ensure user exists in graph
        await self._graph_memory.ensure_user_exists(user_id)
        
        return session
    
    async def process_message(
        self,
        session_id: UUID,
        user_message: str,
    ) -> ChatMessage:
        """Process user message and generate tutor response."""
        from src.core.domain.entities import ChatMessage
        from src.core.domain.value_objects import Role
        from src.core.exceptions import EntityNotFoundError, SessionNotActiveError
        
        # Get session
        session = self._sessions.get(session_id)
        if not session:
            raise EntityNotFoundError("Session", str(session_id))
        if not session.is_active:
            raise SessionNotActiveError(str(session_id))
        
        # Create and store user message
        user_msg = ChatMessage(
            session_id=session_id,
            role=Role.USER,
            content=user_message,
        )
        session.add_message(user_msg)
        
        # Get learning context from graph
        # context = await self._graph_memory.get_learning_context(
        #     user_id=session.user_id,
        #     current_message=user_message,
        # )
        
        # TODO: Build system prompt with context
        # TODO: Use TutorAgent for sophisticated response generation
        
        # Generate response (simplified for now)
        messages = session.get_recent_messages(10)
        response_text = await self._chat_model.generate(messages)
        
        # Create assistant message
        assistant_msg = ChatMessage(
            session_id=session_id,
            role=Role.ASSISTANT,
            content=response_text,
        )
        session.add_message(assistant_msg)
        
        # TODO: Extract vocabulary and errors from conversation
        # TODO: Store in graph memory
        
        return assistant_msg
    
    async def get_session(self, session_id: UUID) -> LearningSession | None:
        """Get session by ID."""
        return self._sessions.get(session_id)
    
    async def end_session(self, session_id: UUID) -> LearningSession:
        """End an active session."""
        from src.core.exceptions import EntityNotFoundError
        
        session = self._sessions.get(session_id)
        if not session:
            raise EntityNotFoundError("Session", str(session_id))
        
        session.end_session()
        return session
    
    async def get_session_history(self, session_id: UUID) -> list[ChatMessage]:
        """Get all messages from a session."""
        session = self._sessions.get(session_id)
        if not session:
            return []
        return session.messages
