#!/usr/bin/env python3
"""
FastAPI Backend for System Design Interview Companion
"""

import os
import random
import uuid
from datetime import datetime, timedelta
from typing import Dict, Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

from questions import get_system_design_questions
from interviewer import InterviewSession, InterviewerPersona

# Load environment variables
load_dotenv()

# Pydantic models
class StartInterviewRequest(BaseModel):
    pass

class StartInterviewResponse(BaseModel):
    session_id: str
    question: str

class ProcessInputRequest(BaseModel):
    session_id: str
    user_input: str

class ProcessInputResponse(BaseModel):
    interviewer_response: str
    current_phase: str

class EvaluateRequest(BaseModel):
    session_id: str
    section: str
    content: str

class EvaluateResponse(BaseModel):
    feedback: str
    score: Optional[int] = None

# In-memory session storage (in production, use Redis or database)
interview_sessions: Dict[str, InterviewSession] = {}
session_expiry: Dict[str, datetime] = {}

def setup_llm() -> ChatOpenAI:
    """Setup and return configured LangChain LLM."""
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set")

    return ChatOpenAI(
        model="gpt-4",
        temperature=0.7
    )

def cleanup_expired_sessions():
    """Remove expired sessions from memory."""
    current_time = datetime.now()
    expired_sessions = [
        session_id for session_id, expiry_time in session_expiry.items()
        if current_time > expiry_time
    ]

    for session_id in expired_sessions:
        interview_sessions.pop(session_id, None)
        session_expiry.pop(session_id, None)

app = FastAPI(
    title="System Design Interview Companion API",
    description="Backend API for the interactive system design interview tool",
    version="1.0.0"
)

# Add CORS middleware to allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """Health check endpoint."""
    return {"message": "System Design Interview Companion API is running!"}

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "interview-companion-api"}

# Interview endpoints
@app.get("/api/interview/question")
async def get_random_question():
    """Get a random system design question."""
    questions = get_system_design_questions()
    selected_question = random.choice(questions)
    return {"question": selected_question}

@app.post("/api/interview/start", response_model=StartInterviewResponse)
async def start_interview():
    """Start a new interview session with LangChain memory."""
    try:
        cleanup_expired_sessions()

        # Generate session ID
        session_id = str(uuid.uuid4())

        # Get random question
        questions = get_system_design_questions()
        selected_question = random.choice(questions)

        # Setup LLM
        llm = setup_llm()

        # Create interview session with memory
        session = InterviewSession(llm, selected_question)

        # Store session (expires in 2 hours)
        interview_sessions[session_id] = session
        session_expiry[session_id] = datetime.now() + timedelta(hours=2)

        return StartInterviewResponse(
            session_id=session_id,
            question=selected_question
        )

    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to start interview: {str(e)}")

@app.post("/api/interview/process", response_model=ProcessInputResponse)
async def process_interview_input(request: ProcessInputRequest):
    """Process user input through the LangChain interviewer."""
    try:
        cleanup_expired_sessions()

        # Get session
        session = interview_sessions.get(request.session_id)
        if not session:
            raise HTTPException(status_code=404, detail="Interview session not found or expired")

        # Process input through LangChain
        interviewer_response = session.process_candidate_input(request.user_input)

        # Update session expiry
        session_expiry[request.session_id] = datetime.now() + timedelta(hours=2)

        return ProcessInputResponse(
            interviewer_response=interviewer_response,
            current_phase=session.get_current_phase_name()
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process input: {str(e)}")

@app.post("/api/interview/evaluate", response_model=EvaluateResponse)
async def evaluate_section(request: EvaluateRequest):
    """Evaluate a specific section using the AI interviewer."""
    try:
        cleanup_expired_sessions()

        # Get session
        session = interview_sessions.get(request.session_id)
        if not session:
            raise HTTPException(status_code=404, detail="Interview session not found or expired")

        # Create evaluation prompt
        evaluation_prompt = f"""
        As an experienced system design interviewer, evaluate the following section from a candidate's interview:

        Section: {request.section}
        Content: {request.content}
        Question: {session.question}

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

        # Get AI evaluation through the session's LLM
        from langchain.schema import SystemMessage, HumanMessage

        messages = [
            SystemMessage(content="You are a senior system design interviewer providing brief, constructive feedback."),
            HumanMessage(content=evaluation_prompt)
        ]

        response = session.llm.invoke(messages)

        # Update session expiry
        session_expiry[request.session_id] = datetime.now() + timedelta(hours=2)

        # Extract score from response (simple pattern matching)
        score = None
        content = response.content
        if "/5" in content:
            import re
            score_match = re.search(r'(\d)/5', content)
            if score_match:
                score = int(score_match.group(1))

        return EvaluateResponse(
            feedback=content,
            score=score
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to evaluate section: {str(e)}")

@app.delete("/api/interview/{session_id}")
async def end_interview(session_id: str):
    """End an interview session and clean up memory."""
    try:
        # Remove session
        interview_sessions.pop(session_id, None)
        session_expiry.pop(session_id, None)

        return {"message": "Interview session ended successfully"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to end interview: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)