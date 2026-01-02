"""
LLM Teacher Adapter - Driven Adapter

Implements the teacher port from the core domain by delegating to an LLM client.

This adapter is part of the hexagonal architecture's "driven" side (right side),
connecting the core domain to external LLM services.

Responsibilities:
- Construct appropriate system prompts based on TeacherProfile
- Delegate message generation to the configured LLM client
- Pass domain entities (ChatMessage, TeacherProfile) to infrastructure
"""

from src.core.domain.entities import ChatMessage
from src.core.domain.value_objects import TeacherProfile, Language
from src.infrastructure.ai.client import LLMClient


class LLMTeacherAdapter:
    """
    Adapter that implements the teacher port by delegating to LLM services.
    
    This driven adapter translates domain needs (conversation history, teacher profile)
    into LLM requests, enabling the core to remain independent of specific LLM implementations.
    """

    def __init__(self, client: LLMClient) -> None:
        """
        Initialize the adapter with an LLM client.
        
        Args:
            client: LLM client implementing the LLMClient protocol.
        """
        self._client = client

    async def get_teacher_response(
        self,
        history: tuple[ChatMessage, ...],
        teacher_profile: TeacherProfile,
        native_lang: Language,
        target_lang: Language,
    ) -> str:
        """
        Generate a teacher's response tailored to the student's learning context.
        
        Uses the conversation history, teacher configuration, and language pair
        to generate an appropriate pedagogical response.
        
        Args:
            history: Conversation history as ChatMessage entities.
            teacher_profile: Teacher behavior configuration (teaching style, corrections level, etc).
            native_lang: Student's native language.
            target_lang: Language being learned by the student.
            
        Returns:
            Teacher's response as a string.
            
        Raises:
            TeacherResponseError: If the teacher service fails to generate a response.
        """
        system_prompt = self._build_system_prompt(teacher_profile, native_lang, target_lang)

        return await self._client.generate(history, system_prompt)

    def _build_system_prompt(
        self, 
        teacher_profile: TeacherProfile,
        native_lang: Language,
        target_lang: Language,
    ) -> str:
        """
        Construct a system prompt for the LLM based on teaching context.
        
        Args:
            teacher_profile: Pedagogical instructions and teaching style configuration.
            native_lang: Student's native language.
            target_lang: Target language being taught.
            
        Returns:
            System prompt string containing role, context, and pedagogical guidelines.
        """
        base_prompt = (
            f"You are an expert language teacher specializing in teaching {target_lang.code} "
            f"to speakers of {native_lang.code}.\n\n"
            "CORE MISSION:\n"
            "1. Engage the student in natural conversation.\n"
            "2. Correct their mistakes subtly but effectively.\n"
            "3. Adapt your vocabulary and grammar to their proficiency level.\n"
            "4. Encourage them to speak more.\n\n"
        )

        style_instructions = {
            "practice": "Focus on creating small exercises and drills. Ask them to conjugate verbs or translate sentences.",
            "explanatory": "Be verbose. Explain the grammar rules behind every correction. Use the student's native language for complex explanations.",
            "corrective": "Be strict. Point out every single mistake. Ask the student to rewrite their sentence correctly before moving on.",
            "conversational": "Prioritize flow. Only correct major errors that impede understanding. Keep the conversation going naturally."
        }

        tone_instructions = {
            0: "Formal, academic, and concise.",
            1: "Professional but encouraging.",
            2: "Friendly, casual, and warm.",
            3: "Very enthusiastic, using emojis and slang appropriate for the target language."
        }

        profile_prompt = (
            "PEDAGOGICAL STYLE:\n"
            f"- Approach: {style_instructions.get(teacher_profile.generation_style.value, 'Conversational')}\n"
            f"- Tone: {tone_instructions.get(teacher_profile.creativity_level.value, 'Friendly')}\n\n"
        )

        rules = (
            "CRITICAL RULES:\n"
            f"- Primarily speak in {target_lang.code}, unless explaining a complex concept.\n"
            "- If the student speaks in their native language, translate it and ask them to repeat it in the target language.\n"
            "- Keep your responses concise (under 3 paragraphs) unless asked to explain.\n"
            "- Do not hallucinate words. If unsure, ask for clarification."
        )

        return base_prompt + profile_prompt + rules