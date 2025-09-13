#!/usr/bin/env python3
"""
System Design Interview Assistant
A simple program to practice system design interviews with random questions.
"""

import os
import random
import sys
from typing import List

from questions import get_system_design_questions


def get_api_key() -> str:
    """
    Safely retrieve OpenAI API key from environment variables.
    
    Returns:
        str: The OpenAI API key
        
    Raises:
        SystemExit: If API key is not found
    """
    api_key = os.getenv('OPENAI_API_KEY')
    
    if not api_key:
        print("❌ Error: OPENAI_API_KEY environment variable not set!")
        print("💡 Please set your API key using:")
        print("   export OPENAI_API_KEY='your-api-key-here'")
        sys.exit(1)
    
    return api_key



def select_random_question(questions: List[str]) -> str:
    """
    Select a random question from the list.
    
    Args:
        questions: List of system design questions
        
    Returns:
        str: A randomly selected question
    """
    return random.choice(questions)


def main():
    """Main program entry point."""
    
    # Verify API key is available (for future LangChain integration)
    get_api_key()
    
    # Welcome message
    print("\n" + "="*60)
    print("🎯 SYSTEM DESIGN INTERVIEW BEGINS! 🎯")
    print("="*60)
    print("📚 Welcome to your system design practice session!")
    print("🚀 Let's sharpen those architectural skills!\n")
    
    # Get questions and select one randomly
    questions = get_system_design_questions()
    selected_question = select_random_question(questions)
    
    # Simulate interviewer
    print("👨‍💼 INTERVIEWER:")
    print(f"\"Hello I am your virtual interviewer! Today we'll be working on this challenge:\"\n")
    print(f"💡 {selected_question}")
    print("\n🤔 \"Take your time to think about the requirements and constraints.\"")
    print("📝 \"Feel free to ask me any clarifying questions!\"\n")
    
    print("="*60)
    print("✨ Practice session initialized! Good luck! ✨")
    print("="*60)


if __name__ == "__main__":
    main()