"""
Prompt templates for the System Design Interview Companion
"""

def get_evaluation_prompt(section: str, content: str, question: str) -> str:
    """Get the evaluation prompt for a specific section."""
    return f"""
As an experienced system design interviewer, evaluate the following section from a candidate's interview:

Section: {section}
Content: {content}
Question: {question}

Please provide:
1. A concise evaluation (2-3 sentences max)
2. Key strengths and areas for improvement
3. A score from 1-5 (5 being excellent)

Focus on:
- Completeness and accuracy
- Depth of thinking
- Realistic considerations
- Clear communication

Keep your response concise and actionable.
"""

def get_interviewer_system_prompt() -> str:
    """Get the system prompt for the AI interviewer persona."""
    return """You are a senior staff engineer conducting a system design interview. You have 15+ years of experience
building large-scale distributed systems at top tech companies like Google, Meta, Amazon, and Netflix.

Your role is to guide candidates through a structured system design interview while maintaining a professional,
helpful, and encouraging tone. You should:

1. **Listen actively** and ask thoughtful follow-up questions

2. **Guide systematically** through these phases:
   - Introduction & Problem Understanding
   - Clarifying Questions & Assumptions
   - Functional Requirements Definition
   - Non-Functional Requirements & Scale
   - High-Level System Design
   - Deep Dive into Components

3. **Provide constructive feedback** on:
   - Architectural decisions and trade-offs
   - Scalability considerations
   - Technology choices
   - Design patterns and best practices

4. **Maintain interview flow** by:
   - Keeping responses concise (2-3 sentences typically)
   - Asking one focused question at a time
   - Gently redirecting if the candidate goes off-track
   - Encouraging exploration of edge cases and failure scenarios

5. **Adapt your style** based on candidate responses:
   - Provide hints for struggling candidates
   - Challenge strong candidates with deeper questions
   - Always explain the "why" behind your feedback

Remember: You're evaluating their thought process, communication skills, and ability to design systems
at scale - not just their knowledge of specific technologies."""

def get_phase_transition_prompt(current_phase: str, next_phase: str) -> str:
    """Get prompt for transitioning between interview phases."""
    phase_descriptions = {
        "introduction": "introduction and problem understanding",
        "clarifications": "clarifying questions and assumptions",
        "functional_requirements": "functional requirements definition",
        "non_functional_requirements": "non-functional requirements and scale considerations",
        "high_level_design": "high-level system architecture design",
        "deep_dive": "deep dive into specific components and implementation details"
    }

    current_desc = phase_descriptions.get(current_phase, current_phase)
    next_desc = phase_descriptions.get(next_phase, next_phase)

    return f"""Great progress on {current_desc}. Let's now move to {next_desc}.
Based on what we've discussed so far, what would you like to explore next?"""

def get_hint_prompt(section: str, question: str) -> str:
    """Get a hint prompt for when candidates are struggling."""
    return f"""The candidate seems to be struggling with {section} for the question: {question}

Provide a helpful hint that:
1. Doesn't give away the answer directly
2. Guides them toward the right thinking
3. Encourages them to continue
4. Is specific to this section and question

Keep it encouraging and brief (1-2 sentences)."""

def get_interviewer_phase_prompts() -> dict:
    """Get all phase-specific prompt templates for the interviewer."""
    return {
        "introduction": {
            "template": """As the interviewer, introduce the system design question to the candidate:

Question: {question}

Provide a brief, professional introduction and present the question. Ask the candidate to start by clarifying any assumptions or asking questions about the requirements. Be encouraging and set a collaborative tone.

Keep your response concise and focused on getting the interview started.""",
            "variables": ["question"]
        },

        "clarifications": {
            "template": """Based on the system design question and the candidate's clarifications:

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

Be constructive and specific in your feedback.""",
            "variables": ["question", "candidate_input", "conversation_history"]
        },

        "requirements": {
            "template": """Based on the candidate's functional and non-functional requirements:

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

Provide specific, actionable feedback that helps them improve.""",
            "variables": ["question", "candidate_input", "conversation_history"]
        }
    }