#!/usr/bin/env python3
"""
Simple AI Coding Agent - Main CLI Interface
"""

import os
import sys
from dotenv import load_dotenv
from agent import CodingAgent


def main():
    """Main entry point for the CLI."""
    print("=" * 60)
    print("Simple AI Coding Agent")
    print("=" * 60)

    # Load environment variables from .env
    load_dotenv()

    # Get API key
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        print("\n❌ Error: ANTHROPIC_API_KEY not found in .env file")
        print("Please create a .env file with your API key:")
        print("  ANTHROPIC_API_KEY=your_key_here")
        sys.exit(1)

    print("\n✓ API key loaded")

    # Create agent
    agent = CodingAgent(api_key=api_key)
    print("✓ Agent initialized with Claude 3.5 Sonnet")
    print("\n💡 Commands:")
    print("  - 'exit' or 'quit': End the session")
    print("  - '/reset': Clear conversation history")
    print("  - '/history': Show conversation stats")

    # Continuous session loop
    try:
        while True:
            # Get user prompt
            print("\n" + "=" * 60)
            print("What would you like me to help you code?")
            print("=" * 60)

            user_prompt = input("\n> ").strip()

            # Check for exit commands
            if user_prompt.lower() in ['exit', 'quit', '/exit', '/quit']:
                print("\n👋 Goodbye!")
                break

            # Check for reset command
            if user_prompt.lower() == '/reset':
                agent.reset_conversation()
                continue

            # Check for history command
            if user_prompt.lower() == '/history':
                msg_count = agent.get_conversation_length()
                print(f"\n📊 Conversation stats:")
                print(f"  - Messages in history: {msg_count}")
                print(f"  - Use '/reset' to clear history")
                continue

            if not user_prompt:
                print("⚠️  Empty prompt. Please enter a task or type 'exit' to quit.")
                continue

            print(f"\n\nRunning agent with prompt:\n{user_prompt}\n")

            # Run the agent
            try:
                result = agent.run(user_prompt)
                print("\n" + "=" * 60)
                print("✅ Task completed!")
                print("=" * 60)
            except Exception as e:
                print(f"\n\n❌ Error: {e}")
                import traceback
                traceback.print_exc()
                print("\n⚠️  Continuing to next task...")

    except KeyboardInterrupt:
        print("\n\n👋 Interrupted by user. Goodbye!")
    except EOFError:
        print("\n\n👋 Goodbye!")


if __name__ == "__main__":
    main()
