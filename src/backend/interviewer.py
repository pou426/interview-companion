"""
Interviewer Module
Contains the AI interviewer persona, prompts, and interview flow logic.
"""

from enum import Enum
from typing import Dict, List, Optional
from langchain.prompts import PromptTemplate
from langchain_core.chat_history import BaseChatMessageHistory, InMemoryChatMessageHistory
from langchain.schema import BaseMessage, SystemMessage, HumanMessage


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

    SYSTEM_PROMPT = """You are a Senior Staff Software Engineer conducting a system design interview. You have 15+ years of experience at top tech companies (Google, Meta, Amazon, Netflix) and have conducted hundreds of system design interviews.

Your expertise includes:
- Distributed systems architecture
- Scalability and performance optimization
- Database design and data modeling
- Microservices and service-oriented architecture
- Load balancing, caching, and CDNs
- Security and reliability patterns
- Real-world trade-offs and engineering decisions

Your interviewing style:
- Professional but friendly and encouraging
- Ask probing follow-up questions to test depth of understanding
- Provide constructive guidance when candidates struggle
- Focus on practical, real-world considerations
- Help candidates think through trade-offs systematically
- Give specific, actionable feedback with examples

You should evaluate candidates on:
- Problem-solving approach and methodology
- Technical depth and breadth
- Communication and explanation skills
- Consideration of trade-offs and constraints
- Scalability thinking
- Real-world practicality

Always maintain the perspective of an experienced engineer who wants to see the candidate succeed while ensuring they demonstrate the required competencies for the role."""

    @staticmethod
    def get_phase_prompt(phase: InterviewPhase) -> PromptTemplate:
        """Get the prompt template for a specific interview phase."""

        prompts = {
            InterviewPhase.INTRODUCTION: PromptTemplate(
                input_variables=["question"],
                template="""As the interviewer, introduce the system design question to the candidate:

Question: {question}

Provide a brief, professional introduction and present the question. Ask the candidate to start by clarifying any assumptions or asking questions about the requirements. Be encouraging and set a collaborative tone.

Keep your response concise and focused on getting the interview started."""
            ),

            InterviewPhase.CLARIFICATIONS: PromptTemplate(
                input_variables=["question", "candidate_input", "conversation_history"],
                template="""Based on the system design question and the candidate's clarifications:

Question: {question}
Candidate's clarifications/assumptions: {candidate_input}

Previous conversation:
{conversation_history}

As an experienced interviewer, evaluate their clarifications and provide feedback:

1. **Assessment (Rate 1-5):**
   - Did they ask relevant clarifying questions?
   - Did they identify key assumptions appropriately?
   - Did they consider user scale, data volume, or constraints?

2. **Feedback:**
   - What they did well
   - What important aspects they missed
   - Specific suggestions for improvement

3. **Guidance:**
   - Additional clarifying questions they should consider
   - Key constraints or assumptions they should be aware of

Then transition them to the next phase: "Now that we've clarified the requirements, let's define the functional and non-functional requirements for this system."

Be constructive and specific in your feedback."""
            ),

            InterviewPhase.REQUIREMENTS: PromptTemplate(
                input_variables=["question", "candidate_input", "conversation_history"],
                template="""Based on the candidate's functional and non-functional requirements:

Question: {question}
Candidate's requirements: {candidate_input}

Previous conversation:
{conversation_history}

As an experienced interviewer, evaluate their requirements definition:

1. **Assessment (Rate 1-5):**
   - Completeness of functional requirements
   - Appropriateness of non-functional requirements (scale, performance, reliability)
   - Understanding of system constraints and trade-offs

2. **Feedback:**
   - Well-identified requirements
   - Missing critical requirements
   - Unrealistic or unnecessary requirements

3. **Guidance:**
   - Essential requirements they missed
   - Scale estimates and performance targets to consider
   - Reliability and availability expectations

Then guide them to the next phase: "Great! Now let's move to the high-level system design. Can you draw out the main components and how they interact?"

Provide specific, actionable feedback that helps them improve."""
            )
        }

        return prompts.get(phase)


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
            SystemMessage(content=InterviewerPersona.SYSTEM_PROMPT),
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