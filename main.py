#!/usr/bin/env python3
"""
Simple AI Coding Agent - Main CLI Interface
"""

import os
import sys
from dotenv import load_dotenv
from agent import CodingAgent
from ui import (
    print_header, print_success, print_error, print_warning, print_info,
    info, bold, dim
)


def main():
    """Main entry point for the CLI."""
    print_header("Simple AI Coding Agent")

    # Load environment variables from .env
    load_dotenv()

    # Get API key
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        print()
        print_error("ANTHROPIC_API_KEY not found in .env file")
        print("Please create a .env file with your API key:")
        print(dim("  ANTHROPIC_API_KEY=your_key_here"))
        sys.exit(1)

    print()
    print_success("API key loaded")

    # Create agent
    agent = CodingAgent(api_key=api_key)
    print_success("Agent initialized with Claude 3.5 Sonnet")
    print()
    print_info("Available commands:")
    print(dim("  - 'exit' or 'quit': End the session"))
    print(dim("  - '/reset': Clear conversation history"))
    print(dim("  - '/history': Show conversation stats"))

    # Continuous session loop
    try:
        while True:
            # Get user prompt
            print()
            print_header("What would you like me to help you code?")

            user_prompt = input(f"\n{bold('>')} ").strip()

            # Check for exit commands
            if user_prompt.lower() in ['exit', 'quit', '/exit', '/quit']:
                print()
                print(info("Goodbye!"))
                break

            # Check for reset command
            if user_prompt.lower() == '/reset':
                agent.reset_conversation()
                continue

            # Check for history command
            if user_prompt.lower() == '/history':
                msg_count = agent.get_conversation_length()
                print()
                print_info("Conversation stats:")
                print(dim(f"  - Messages in history: {msg_count}"))
                print(dim("  - Use '/reset' to clear history"))
                continue

            if not user_prompt:
                print_warning("Empty prompt. Please enter a task or type 'exit' to quit.")
                continue

            print(f"\n{dim('Running agent with prompt:')}")
            print(f"{dim(user_prompt)}\n")

            # Run the agent
            try:
                result = agent.run(user_prompt)
                print()
                print_success("Task completed!")
                print()
            except Exception as e:
                print()
                print_error(f"Error: {e}")
                import traceback
                traceback.print_exc()
                print()
                print_warning("Continuing to next task...")

    except KeyboardInterrupt:
        print("\n")
        print(info("Interrupted by user. Goodbye!"))
    except EOFError:
        print("\n")
        print(info("Goodbye!"))


if __name__ == "__main__":
    main()
