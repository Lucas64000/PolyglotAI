
import streamlit as st
import asyncio
import sys
from pathlib import Path
from uuid import UUID, uuid4

current_file = Path(__file__).resolve()
project_root = current_file.parents[5]
sys.path.append(str(project_root))
print(project_root)

from src.core.domain.value_objects import Language, CreativityLevel, GenerationStyle

from src.application.dtos import (
    CreateConversationCommand, 
    SendMessageCommand, 
    SelectConversationQuery,
    ListConversationsQuery,
)

from src.infrastructure.adapters.driving.streamlit import get_container

st.set_page_config(
    page_title="PolyglotAI",
    page_icon="🎓",
    layout="wide"
)

def run_async(coroutine):
    """Execute async code in synchronous Streamlit context."""
    return asyncio.run(coroutine)

if "student_id" not in st.session_state:
    st.session_state.student_id = str(uuid4())

if "current_conversation_id" not in st.session_state:
    st.session_state.current_conversation_id = None

# Dependency injection container
container = get_container()

with st.sidebar:
    st.header("👤 Student Profile")
    student_id_input = st.text_input("Student UUID", value=st.session_state.student_id)
    if student_id_input != st.session_state.student_id:
        st.session_state.student_id = student_id_input
        st.session_state.current_conversation_id = None
        st.rerun()

    st.divider()

    st.header("💬 Conversations")
    
    with st.expander("➕ New Conversation", expanded=False):
        with st.form("new_conv_form"):
            native = st.text_input("Native Language", value="fr", max_chars=2, help="ISO code (e.g. fr)")
            target = st.text_input("Target Language", value="en", max_chars=2, help="ISO code (e.g. en)")
            title = st.text_input("Title (Optional)", placeholder="My Lesson")
            submitted = st.form_submit_button("Start Learning")
            if submitted:
                try:
                    cmd = CreateConversationCommand(
                        student_id=UUID(st.session_state.student_id),
                        title=title if title else None,
                        native_lang=Language(native),
                        target_lang=Language(target)
                    )
                    result = run_async(container.create_conversation_use_case.execute(cmd))
                    
                    st.session_state.current_conversation_id = str(result.conversation_id)
                    st.rerun()
                except Exception as e:
                    st.error(f"Error: {str(e)}")

    try:
        query = ListConversationsQuery(
            student_id=UUID(st.session_state.student_id),
            limit=10,
            offset=0
        )
        conversations = run_async(
            container.list_conversations_use_case.execute(query=query)
        )
        
        st.caption("Recent")
        for conv in conversations:
            btn_label = f"{'🟢' if conv.status == 'ACTIVE' else '⚪'} {conv.title}"
            if st.button(btn_label, key=str(conv.conversation_id), use_container_width=True):
                st.session_state.current_conversation_id = str(conv.conversation_id)
                st.rerun()
                
    except Exception as e:
        st.error("Could not load history.")


if not st.session_state.current_conversation_id:
    st.title("Welcome to PolyglotAI 🎓")
    st.info("👈 Select a conversation or create a new one to start.")
else:
    try:
        current_id = UUID(st.session_state.current_conversation_id)
        query = SelectConversationQuery(
            conversation_id=current_id,
            student_id=UUID(st.session_state.student_id)
        )

        conversation_dto = run_async(
            container.select_conversation_use_case.execute(query=query)
        )
        
        st.title(conversation_dto.title)
        st.caption(f"Learning {conversation_dto.target_lang} from {conversation_dto.native_lang}")

        for msg in conversation_dto.messages:
            with st.chat_message(msg.role.lower()):
                st.markdown(msg.content)
        
        if prompt := st.chat_input("Enter your message..."):
            with st.chat_message("student"):
                st.markdown(prompt)

            with st.chat_message("teacher"):
                with st.spinner("Generating response..."):
                    try:
                        cmd = SendMessageCommand(
                            conversation_id=current_id,
                            student_message=prompt,
                            creativity_level=CreativityLevel.MODERATE,
                            generation_style=GenerationStyle.CONVERSATIONAL
                        )
                        response_dto = run_async(container.send_message_use_case.execute(cmd))
                        
                        st.markdown(response_dto.teacher_message)    
                            
                    except Exception as e:
                        st.error(f"Error: {str(e)}")

    except Exception as e:
        st.error(f"Error loading conversation: {str(e)}")
        if st.button("Back to Home"):
            st.session_state.current_conversation_id = None
            st.rerun()