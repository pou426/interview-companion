"""
Interviewer Module
Contains the AI interviewer persona, prompts, and interview flow logic.
"""

from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain.schema import SystemMessage, HumanMessage

class InterviewSession:
    """Manages an interactive interview session with memory and contextual tracking."""

    def __init__(self, llm, question: str):
        """Initialize interview session."""
        self.llm = llm
        self.question = question
        self.memory = InMemoryChatMessageHistory()
        self.user_sections = {
            'assumptions': '',
            'functionalRequirements': '',
            'nonFunctionalRequirements': '',
            'resourceEstimation': '',
            'highLevelDesign': '',
            'deepDive': ''
        }

        # Initialize conversation with the interview question
        initial_context = f"Interview started for question: {question}"
        self.memory.add_user_message(initial_context)
        self.memory.add_ai_message("Interview session initialized. Ready to provide contextual feedback.")

    def update_section(self, section: str, content: str):
        """Update user's work on a specific section and track changes."""
        previous_content = self.user_sections.get(section, '')
        self.user_sections[section] = content

        # Track evolution of thinking if there was previous content
        if previous_content.strip() and content.strip() and previous_content != content:
            change_summary = self._analyze_content_change(section, previous_content, content)
            self.memory.add_user_message(f"Evolved thinking in {section}: {change_summary}")
        elif content.strip() and not previous_content.strip():
            self.memory.add_user_message(f"Initial approach for {section}")

    def _analyze_content_change(self, section: str, old_content: str, new_content: str) -> str:
        """Analyze how the user's approach evolved in a section."""
        # Simple heuristic-based change analysis
        if len(new_content) > len(old_content) * 1.5:
            return "significantly expanded their approach"
        elif len(new_content) < len(old_content) * 0.7:
            return "simplified and refined their approach"
        elif any(word in new_content.lower() for word in ['microservice', 'distributed', 'cache', 'queue', 'load balancer']):
            if not any(word in old_content.lower() for word in ['microservice', 'distributed', 'cache', 'queue', 'load balancer']):
                return "moved from basic to more distributed architecture approach"
        return "refined their approach with additional considerations"

    def get_full_context(self) -> str:
        """Get the full context of all user's work so far."""
        context_parts = []
        context_parts.append(f"Interview Question: {self.question}")

        section_names = {
            'assumptions': 'Assumptions & Clarifying Questions',
            'functionalRequirements': 'Functional Requirements',
            'nonFunctionalRequirements': 'Non-Functional Requirements',
            'resourceEstimation': 'Resource Estimation Notes',
            'highLevelDesign': 'High-Level Components & Design',
            'deepDive': 'Deep Dive Topics'
        }

        for section_key, content in self.user_sections.items():
            if content.strip():
                section_name = section_names.get(section_key, section_key)
                context_parts.append(f"\n{section_name}:\n{content}")

        return "\n".join(context_parts)

    def evaluate_section_with_context(self, section: str, content: str) -> str:
        """Evaluate a section with full interview context."""
        # Update the section content
        self.update_section(section, content)

        # Get full context
        full_context = self.get_full_context()

        # Create section-focused evaluation prompt with contextual references
        evaluation_prompt = f"""As a senior staff software engineer, evaluate the {section} section concisely:

Content: {content}
Question: {self.question}
Context: {full_context}
Evolution: {self._get_conversation_history()}

Provide brief feedback (3-4 sentences max):
1. What's good and what's missing in {section}
2. One key improvement needed
3. Score: X/5 with brief reason

Be specific, actionable, and encouraging."""

        # Create messages for LLM
        messages = [
            SystemMessage(content="You are a senior staff software engineer providing brief, constructive system design interview feedback. Keep responses concise (3-4 sentences max)."),
            HumanMessage(content=evaluation_prompt)
        ]

        # Get AI response
        response = self.llm.invoke(messages)

        # Add evaluation to memory for future context
        self.memory.add_ai_message(f"Evaluation for {section}: {response.content}")

        return response.content

    def _get_conversation_history(self) -> str:
        """Get formatted conversation history."""
        messages = self.memory.messages
        history = []
        for msg in messages[-10:]:  # Last 10 messages for context
            if hasattr(msg, 'content') and msg.content:
                role = "AI Interviewer" if msg.type == "ai" else "Candidate"
                history.append(f"{role}: {msg.content}")
        return "\n".join(history)
