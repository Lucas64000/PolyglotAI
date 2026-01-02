
from functools import lru_cache

from src.infrastructure.adapters.driving.fastapi.dependencies import (
    get_in_memory_db,
    get_chat_provider,
    get_time_provider,
    get_create_conversation_use_case,
    get_list_conversations_use_case,
    get_select_conversation_use_case,
    get_send_message_use_case,
    get_conversation_repository,
    get_conversation_reader,
)

class Container:
    """
    Dependency injection container for Streamlit.
    """
    
    @property
    def create_conversation_use_case(self):
        db = get_in_memory_db()
        repo = get_conversation_repository(db)
        time = get_time_provider()
        return get_create_conversation_use_case(repository=repo, time_provider=time)

    @property
    def list_conversations_use_case(self):
        db = get_in_memory_db()
        reader = get_conversation_reader(db)
        return get_list_conversations_use_case(reader=reader)

    @property
    def select_conversation_use_case(self):
        db = get_in_memory_db()
        repo = get_conversation_repository(db)
        return get_select_conversation_use_case(repository=repo)

    @property
    def send_message_use_case(self):
        chat = get_chat_provider()
        db = get_in_memory_db()
        repo = get_conversation_repository(db)
        time = get_time_provider()
        return get_send_message_use_case(
            chat_provider=chat, 
            repository=repo, 
            time_provider=time,
        )

@lru_cache
def get_container() -> Container:
    """Get singleton instance of DI container."""
    return Container()