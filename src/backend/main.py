#!/usr/bin/env python3
"""
FastAPI Backend for System Design Interview Companion
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

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

# Placeholder for future interview endpoints
@app.post("/api/interview/start")
async def start_interview():
    """Start a new interview session (placeholder)."""
    return {"message": "Interview starting soon!", "status": "not_implemented"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)