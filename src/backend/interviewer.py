"""
Interviewer Module
Contains the AI interviewer persona, prompts, and interview flow logic.
"""

from enum import Enum
from typing import Dict, List, Optional
from langchain.prompts import PromptTemplate
from langchain_core.chat_history import BaseChatMessageHistory, InMemoryChatMessageHistory
from langchain.schema import BaseMessage, SystemMessage, HumanMessage
from prompts import get_interviewer_system_prompt, get_interviewer_phase_prompts


class InterviewPhase(Enum):
    """Enumeration of interview phases."""
    INTRODUCTION = "introduction"
    CLARIFICATIONS = "clarifications"
    REQUIREMENTS = "requirements"
    HIGH_LEVEL_DESIGN = "high_level_design"
    DEEP_DIVE = "deep_dive"
    WRAP_UP = "wrap_up"


class InterviewerPersona:
    """Defines the AI interviewer persona and behavior."""

    @staticmethod
    def get_system_prompt() -> str:
        """Get the system prompt for the interviewer."""
        return get_interviewer_system_prompt()

    @staticmethod
    def get_phase_prompt(phase: InterviewPhase) -> PromptTemplate:
        """Get the prompt template for a specific interview phase."""
        phase_prompts = get_interviewer_phase_prompts()

        phase_map = {
            InterviewPhase.INTRODUCTION: "introduction",
            InterviewPhase.CLARIFICATIONS: "clarifications",
            InterviewPhase.REQUIREMENTS: "requirements"
        }

        phase_key = phase_map.get(phase)
        if not phase_key or phase_key not in phase_prompts:
            return None

        prompt_data = phase_prompts[phase_key]
        return PromptTemplate(
            input_variables=prompt_data["variables"],
            template=prompt_data["template"]
        )


class InterviewSession:
    """Manages an interactive interview session with memory and phase tracking."""

    def __init__(self, llm, question: str):
        """Initialize interview session."""
        self.llm = llm
        self.question = question
        self.current_phase = InterviewPhase.INTRODUCTION
        self.memory = InMemoryChatMessageHistory()
        self.phase_scores = {}

    def get_current_phase_name(self) -> str:
        """Get human-readable current phase name."""
        phase_names = {
            InterviewPhase.INTRODUCTION: "Introduction",
            InterviewPhase.CLARIFICATIONS: "Clarifications & Assumptions",
            InterviewPhase.REQUIREMENTS: "Requirements Definition",
            InterviewPhase.HIGH_LEVEL_DESIGN: "High-Level Design",
            InterviewPhase.DEEP_DIVE: "Deep Dive",
            InterviewPhase.WRAP_UP: "Wrap Up"
        }
        return phase_names.get(self.current_phase, "Unknown")

    def advance_phase(self):
        """Advance to the next interview phase."""
        phases = list(InterviewPhase)
        current_index = phases.index(self.current_phase)
        if current_index < len(phases) - 1:
            self.current_phase = phases[current_index + 1]

    def get_conversation_history(self) -> str:
        """Get formatted conversation history."""
        messages = self.memory.messages
        history = []
        for msg in messages:
            if hasattr(msg, 'content'):
                role = "Interviewer" if msg.type == "ai" else "Candidate"
                history.append(f"{role}: {msg.content}")
        return "\n".join(history)

    def process_candidate_input(self, user_input: str) -> str:
        """Process candidate input and generate interviewer response."""

        # Add user input to memory
        self.memory.add_user_message(user_input)

        # Get appropriate prompt for current phase
        prompt_template = InterviewerPersona.get_phase_prompt(self.current_phase)

        if not prompt_template:
            return "I'm not sure how to proceed. Let's continue with the discussion."

        # Format prompt based on current phase
        if self.current_phase == InterviewPhase.INTRODUCTION:
            formatted_prompt = prompt_template.format(question=self.question)
        else:
            conversation_history = self.get_conversation_history()
            formatted_prompt = prompt_template.format(
                question=self.question,
                candidate_input=user_input,
                conversation_history=conversation_history
            )

        # Create messages with system prompt
        messages = [
            SystemMessage(content=InterviewerPersona.get_system_prompt()),
            HumanMessage(content=formatted_prompt)
        ]

        # Get AI response
        response = self.llm.invoke(messages)

        # Add AI response to memory
        self.memory.add_ai_message(response.content)

        # Advance phase after certain phases
        if self.current_phase in [InterviewPhase.CLARIFICATIONS, InterviewPhase.REQUIREMENTS]:
            self.advance_phase()

        return response.content