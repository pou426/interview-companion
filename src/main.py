#!/usr/bin/env python3
"""
System Design Interview Assistant
A simple program to practice system design interviews with random questions.
"""

import os
import random
import sys
from typing import List
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

from questions import get_system_design_questions
from interviewer import InterviewSession, InterviewerPersona, InterviewPhase


def setup_environment() -> ChatOpenAI:
    """
    Setup environment and initialize LangChain LLM.

    Returns:
        ChatOpenAI: Configured OpenAI LLM instance

    Raises:
        SystemExit: If API key is not found
    """
    # Load environment variables
    load_dotenv()

    api_key = os.getenv('OPENAI_API_KEY')

    if not api_key:
        print("❌ Error: OPENAI_API_KEY environment variable not set!")
        print("💡 Please set your API key using:")
        print("   export OPENAI_API_KEY='your-api-key-here'")
        print("   Or create a .env file with OPENAI_API_KEY=your-key")
        sys.exit(1)

    # Initialize LangChain OpenAI LLM
    llm = ChatOpenAI(
        model="gpt-4",
        temperature=0.7
    )

    return llm



def select_random_question(questions: List[str]) -> str:
    """
    Select a random question from the list.
    
    Args:
        questions: List of system design questions
        
    Returns:
        str: A randomly selected question
    """
    return random.choice(questions)


def run_interactive_interview(session: InterviewSession):
    """
    Run the interactive interview session.

    Args:
        session: The interview session instance
    """

    print("\n" + "="*70)
    print("🎯 INTERACTIVE SYSTEM DESIGN INTERVIEW 🎯")
    print("="*70)
    print("📝 This is a structured interview with multiple phases:")
    print("   1️⃣ Clarifications & Assumptions")
    print("   2️⃣ Functional & Non-Functional Requirements")
    print("   3️⃣ High-Level Design")
    print("   4️⃣ Deep Dive")
    print("   5️⃣ Wrap Up")
    print("\n💡 The AI interviewer will provide feedback after each phase.")
    print("📋 Type 'quit' to exit, 'help' for commands")
    print("="*70)

    # Start with introduction
    if session.current_phase == InterviewPhase.INTRODUCTION:
        intro_response = session.process_candidate_input("Please start the interview")
        print(f"\n🎙️ INTERVIEWER:\n{intro_response}\n")
        session.advance_phase()

    # Main interview loop
    while session.current_phase != InterviewPhase.WRAP_UP:
        phase_name = session.get_current_phase_name()
        print(f"\n📍 CURRENT PHASE: {phase_name}")
        print("-" * 50)

        # Get user input
        try:
            user_input = input("\n👤 YOUR RESPONSE: ").strip()

            if user_input.lower() == 'quit':
                print("\n👋 Interview session ended. Good luck with your preparation!")
                break
            elif user_input.lower() == 'help':
                print("\n📋 COMMANDS:")
                print("   quit - Exit the interview")
                print("   help - Show this help message")
                continue
            elif not user_input:
                print("⚠️  Please provide a response or type 'quit' to exit.")
                continue

            # Process input and get interviewer response
            interviewer_response = session.process_candidate_input(user_input)

            # Display interviewer feedback
            print(f"\n🎙️ INTERVIEWER FEEDBACK:")
            print("-" * 30)
            print(f"{interviewer_response}\n")

        except KeyboardInterrupt:
            print("\n\n👋 Interview session interrupted. Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error occurred: {e}")
            print("Please try again or type 'quit' to exit.")

    print("\n" + "="*70)
    print("✨ INTERVIEW COMPLETED! ✨")
    print("="*70)


def main():
    """Main program entry point."""

    try:
        # Setup environment and LLM
        llm = setup_environment()

        # Get questions and select one randomly
        questions = get_system_design_questions()
        selected_question = select_random_question(questions)

        # Create interview session
        session = InterviewSession(llm, selected_question)

        # Run interactive interview
        run_interactive_interview(session)

    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
    except Exception as e:
        print(f"\n❌ Error starting interview: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()