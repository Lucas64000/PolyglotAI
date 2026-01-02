
from typing import Annotated
from fastapi import Depends
from functools import lru_cache

from src.core.ports import ConversationRepository, TimeProvider, ChatProvider
from src.application.ports import ConversationReader

from src.application.commands import (
    CreateConversationUseCase, 
    SendMessageUseCase, 
    DeleteConversationUseCase
)
from src.application.queries import (
    SelectConversationUseCase, 
    ListStudentConversationsUseCase
)

from src.infrastructure.ai import OllamaClient, OllamaConfig
from src.infrastructure.adapters.driven import (
    LLMTeacherAdapter, 
    InMemoryConversationRepository, 
    SystemTimeProvider,
)

# ──────────────────────────────────────────────────────────────────────────────
# SINGLETONS (Shared State)
# ──────────────────────────────────────────────────────────────────────────────

@lru_cache
def get_in_memory_db() -> InMemoryConversationRepository:
    return InMemoryConversationRepository()

@lru_cache
def get_chat_provider() -> ChatProvider:
    config = OllamaConfig()
    client = OllamaClient(
        base_url=config.openai_compatible_url, 
        model_name=config.model
    )
    return LLMTeacherAdapter(client=client)

def get_time_provider() -> TimeProvider:
    return SystemTimeProvider()

# ──────────────────────────────────────────────────────────────────────────────
# PORTS
# ──────────────────────────────────────────────────────────────────────────────

def get_conversation_repository(
    db: InMemoryConversationRepository = Depends(get_in_memory_db)
) -> ConversationRepository:
    return db

def get_conversation_reader(
    db: InMemoryConversationRepository = Depends(get_in_memory_db)
) -> ConversationReader:
    return db

# ──────────────────────────────────────────────────────────────────────────────
# ALIAS PORTS
# ──────────────────────────────────────────────────────────────────────────────

RepoDep = Annotated[ConversationRepository, Depends(get_conversation_repository)]
ReaderDep = Annotated[ConversationReader, Depends(get_conversation_reader)]
TimeDep = Annotated[TimeProvider, Depends(get_time_provider)]
ChatDep = Annotated[ChatProvider, Depends(get_chat_provider)]

# ──────────────────────────────────────────────────────────────────────────────
# USE CASES FACTORIES
# ──────────────────────────────────────────────────────────────────────────────

def get_create_conversation_use_case(
    repository: RepoDep,
    time_provider: TimeDep    
) -> CreateConversationUseCase:
    return CreateConversationUseCase(repository=repository, time_provider=time_provider)

def get_send_message_use_case(
    chat_provider: ChatDep,
    repository: RepoDep,
    time_provider: TimeDep,
) -> SendMessageUseCase:
    return SendMessageUseCase(
        chat_provider=chat_provider, 
        repository=repository, 
        time_provider=time_provider,
    )

def get_select_conversation_use_case(
    repository: RepoDep
) -> SelectConversationUseCase:
    return SelectConversationUseCase(repository=repository)

def get_delete_conversation_use_case(
    repository: RepoDep,
    time_provider: TimeDep
) -> DeleteConversationUseCase:
    return DeleteConversationUseCase(repository=repository, time_provider=time_provider)

def get_list_conversations_use_case(
    reader: ReaderDep
) -> ListStudentConversationsUseCase:
    return ListStudentConversationsUseCase(reader=reader)

# ──────────────────────────────────────────────────────────────────────────────
# ALIAS USE CASES
# ──────────────────────────────────────────────────────────────────────────────

CreateConversationUseCaseDep = Annotated[CreateConversationUseCase, Depends(get_create_conversation_use_case)]
SendMessageUseCaseDep = Annotated[SendMessageUseCase, Depends(get_send_message_use_case)]
SelectConversationUseCaseDep = Annotated[SelectConversationUseCase, Depends(get_select_conversation_use_case)]
DeleteConversationUseCaseDep = Annotated[DeleteConversationUseCase, Depends(get_delete_conversation_use_case)]
ListConversationsUseCaseDep = Annotated[ListStudentConversationsUseCase, Depends(get_list_conversations_use_case)]