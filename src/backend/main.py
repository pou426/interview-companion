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
from interviewer import InterviewSession

# Load environment variables
load_dotenv()

# Pydantic models
class StartInterviewRequest(BaseModel):
    pass

class StartInterviewResponse(BaseModel):
    session_id: str
    question: str


class EvaluateRequest(BaseModel):
    session_id: str
    section: str
    content: str

class EvaluateResponse(BaseModel):
    feedback: str
    score: Optional[int] = None

class ValidateSessionRequest(BaseModel):
    session_id: str

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
    allow_origins=[
        "http://localhost:3000",  # React dev server
        "https://interview-companion-beta.vercel.app",  # Your Vercel deployment
        os.getenv("FRONTEND_URL", "https://interview-companion-beta.vercel.app")  # Production frontend
    ],
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

@app.post("/api/interview/evaluate", response_model=EvaluateResponse)
async def evaluate_section(request: EvaluateRequest):
    """Evaluate a specific section using the AI interviewer."""
    try:
        cleanup_expired_sessions()

        # Get session
        session = interview_sessions.get(request.session_id)
        if not session:
            raise HTTPException(status_code=404, detail="Interview session not found or expired")

        # Use session's contextual evaluation method
        response_content = session.evaluate_section_with_context(request.section, request.content)

        # Update session expiry
        session_expiry[request.session_id] = datetime.now() + timedelta(hours=2)

        # Extract score from response (simple pattern matching)
        score = None
        if "/5" in response_content:
            import re
            score_match = re.search(r'(\d)/5', response_content)
            if score_match:
                score = int(score_match.group(1))

        return EvaluateResponse(
            feedback=response_content,
            score=score
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to evaluate section: {str(e)}")

@app.post("/api/interview/validate")
async def validate_session(request: ValidateSessionRequest):
    """Validate if a session ID is still active."""
    try:
        cleanup_expired_sessions()

        session = interview_sessions.get(request.session_id)
        if not session:
            raise HTTPException(status_code=404, detail="Session not found or expired")

        return {"status": "valid"}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to validate session: {str(e)}")

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
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=False)