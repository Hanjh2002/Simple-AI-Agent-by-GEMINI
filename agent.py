"""
AI Coding Agent with ReAct loop.
Uses Anthropic's Claude API with tool calling.
"""

import os
from typing import List, Dict, Any
from anthropic import Anthropic
from tools import TOOL_SCHEMAS, execute_tool


class CodingAgent:
    """Simple AI coding agent that can read, write, edit files and run shell commands."""

    def __init__(self, api_key: str, model: str = "claude-3-5-sonnet-20241022"):
        """Initialize the agent with API key."""
        self.client = Anthropic(api_key=api_key)
        self.model = model
        self.conversation_history: List[Dict[str, Any]] = []

        # System prompt that guides Claude's behavior
        self.system_prompt = """You are an expert AI coding assistant that helps users with programming tasks.

You have access to tools that allow you to:
- read_file: Read existing files to understand the codebase
- write_file: Create new files or completely overwrite existing ones
- edit_file: Make targeted edits to existing files
- shell_command: Execute shell commands (run tests, install packages, etc.)

When given a coding task, follow this approach:
1. First, use read_file to understand existing code if modifying something
2. Then, use write_file or edit_file to make changes
3. Finally, use shell_command to test or verify your changes if appropriate

Think step by step. Use tools iteratively to accomplish the task.
Always explain what you're doing and why."""

    def run(self, user_prompt: str, max_iterations: int = 15) -> str:
        """
        Run the agent with a user prompt using a ReAct loop.

        Args:
            user_prompt: The user's request
            max_iterations: Maximum number of tool use iterations (prevents infinite loops)

        Returns:
            The final response from Claude
        """
        # Initialize conversation with user's prompt
        self.conversation_history = [
            {
                "role": "user",
                "content": user_prompt
            }
        ]

        iteration = 0

        # ReAct loop: Reason -> Act -> Observe
        while iteration < max_iterations:
            iteration += 1
            print(f"\n{'='*60}")
            print(f"Iteration {iteration}/{max_iterations}")
            print(f"{'='*60}")

            # Call Claude with current conversation history
            response = self.client.messages.create(
                model=self.model,
                max_tokens=4096,
                system=self.system_prompt,
                tools=TOOL_SCHEMAS,
                messages=self.conversation_history
            )

            print(f"\nClaude's response:")
            print(f"Stop reason: {response.stop_reason}")

            # Add Claude's response to conversation history
            assistant_message = {
                "role": "assistant",
                "content": response.content
            }
            self.conversation_history.append(assistant_message)

            # Check if Claude wants to use tools
            if response.stop_reason == "tool_use":
                # Extract tool uses from response
                tool_uses = [block for block in response.content if block.type == "tool_use"]

                # Also show any thinking/text before tool use
                text_blocks = [block for block in response.content if block.type == "text"]
                for text_block in text_blocks:
                    print(f"\nClaude's thinking: {text_block.text}")

                # Execute each tool
                tool_results = []
                for tool_use in tool_uses:
                    print(f"\n[TOOL USE] {tool_use.name}")
                    print(f"Parameters: {tool_use.input}")

                    # Ask for user confirmation for dangerous operations
                    if tool_use.name in ["write_file", "edit_file", "shell_command"]:
                        confirm = input(f"\n⚠️  Allow {tool_use.name}? (y/n): ").strip().lower()
                        if confirm != 'y':
                            print("❌ Tool execution cancelled by user")
                            tool_result = {
                                "success": False,
                                "error": "Tool execution cancelled by user"
                            }
                        else:
                            # Execute the tool
                            tool_result = execute_tool(tool_use.name, tool_use.input)
                    else:
                        # Read-only operations don't need confirmation
                        tool_result = execute_tool(tool_use.name, tool_use.input)

                    print(f"Result: {tool_result}")

                    # Format result for Claude
                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": tool_use.id,
                        "content": str(tool_result)
                    })

                # Add tool results to conversation
                self.conversation_history.append({
                    "role": "user",
                    "content": tool_results
                })

            elif response.stop_reason == "end_turn":
                # Claude is done - extract final text response
                text_blocks = [block for block in response.content if block.type == "text"]
                final_response = "\n".join([block.text for block in text_blocks])

                print(f"\n{'='*60}")
                print(f"FINAL RESPONSE:")
                print(f"{'='*60}")
                print(final_response)

                return final_response

            else:
                # Unexpected stop reason
                print(f"\nUnexpected stop reason: {response.stop_reason}")
                text_blocks = [block for block in response.content if block.type == "text"]
                return "\n".join([block.text for block in text_blocks])

        # Max iterations reached
        return "⚠️ Maximum iterations reached. The task may not be complete."

    def get_conversation_history(self) -> List[Dict[str, Any]]:
        """Get the full conversation history."""
        return self.conversation_history
