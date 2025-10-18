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

    # Get user prompt
    print("\n" + "=" * 60)
    print("What would you like me to help you code?")
    print("=" * 60)

    user_prompt = input("\n> ").strip()

    if not user_prompt:
        print("\n❌ No prompt provided. Exiting.")
        sys.exit(1)

    print(f"\n\nRunning agent with prompt:\n{user_prompt}\n")

    # Run the agent
    try:
        result = agent.run(user_prompt)
        print("\n" + "=" * 60)
        print("Task completed!")
        print("=" * 60)
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user. Exiting...")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
