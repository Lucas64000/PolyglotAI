
from src.services.llm.llm_factory import LLMFactory
from src.services.memory.repositories.json_repository import JsonFileMemoryRepository
from src.services.memory.strategies.window_strategy import WindowMemoryStrategy

from src.models.conversation_model import Message

from src.core.enums import Role
from uuid import uuid4

from src.utils.logger import get_logger

logger = get_logger(__name__)

def main():

    llm = LLMFactory.create_llm_provider(
        provider_name="azure",
        model_name="gpt-4o-mini",
        temperature=0.7,
        max_tokens=1000
    )
    memory = JsonFileMemoryRepository()
    strategy = WindowMemoryStrategy(repository=memory, window_size=5)

    print()
    print("="*60)
    print("Test conversation avec mémoire")
    print("="*60)
    print()
    
    user_id = uuid4()
    conv = memory.create_conversation(user_id=user_id)
    cid = conv.id

    msg_user1 = Message(
        conversation_id=cid,
        role=Role.USER,
        content="Bonjour, je m'appelle Lucas."
    )
    strategy.save_message(msg_user1)
    print(msg_user1)
    
    conversation = strategy.get_context(cid)
    response1 = llm.generate(messages=conversation)
    strategy.save_message(response1)
    print(response1)
    print()

    msg_user2 = Message(
        conversation_id=cid,
        role=Role.USER,
        content="Comment tu va aujourd'hui ?"
    )
    strategy.save_message(msg_user2)
    print(msg_user2)
    
    conversation = strategy.get_context(cid)
    for msg in conversation:
        logger.info(str(msg))

    response2 = llm.generate(messages=conversation)
    strategy.save_message(response2)
    print(response2)
    print()

    msg_user3 = Message(
        conversation_id=cid,
        role=Role.USER,
        content="Tu peux me rappeler mon prénom ? Et j'aimerais que tu me dises si j'ai fait une faute dans la phrase d'avant. Idem avec le message précédent"
    )
    strategy.save_message(msg_user3)
    print(msg_user3)
    
    conversation = strategy.get_context(cid)
    response3 = llm.generate(messages=conversation)
    strategy.save_message(response3)
    print(response3)
    print()

if __name__ == "__main__":
    main()
