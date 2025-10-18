"""
Tools for the AI coding agent.
Each tool has a schema (for Claude) and an execute function.
"""

import os
import subprocess
from typing import Dict, Any, List
from ddgs import DDGS


# Tool schemas for Claude API
TOOL_SCHEMAS = [
    {
        "name": "read_file",
        "description": "Read the contents of a file. Use this to understand existing code or files before making changes. Returns the full file content as a string.",
        "input_schema": {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "The path to the file to read (relative or absolute)"
                }
            },
            "required": ["path"]
        }
    },
    {
        "name": "write_file",
        "description": "Create a new file or completely overwrite an existing file with new content. Use this to create new files from scratch. WARNING: This will overwrite existing files completely.",
        "input_schema": {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "The path where the file should be written"
                },
                "content": {
                    "type": "string",
                    "description": "The complete content to write to the file"
                }
            },
            "required": ["path", "content"]
        }
    },
    {
        "name": "edit_file",
        "description": "Edit an existing file by replacing specific text. Use this to make targeted changes to existing files. Finds the first occurrence of old_text and replaces it with new_text. Returns an error if old_text is not found.",
        "input_schema": {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "The path to the file to edit"
                },
                "old_text": {
                    "type": "string",
                    "description": "The exact text to find and replace (must match exactly)"
                },
                "new_text": {
                    "type": "string",
                    "description": "The new text to replace old_text with"
                }
            },
            "required": ["path", "old_text", "new_text"]
        }
    },
    {
        "name": "shell_command",
        "description": "Execute a shell command and return its output. Use this to run programs, install packages, run tests, etc. Returns stdout, stderr, and the exit code. Be careful with destructive commands.",
        "input_schema": {
            "type": "object",
            "properties": {
                "command": {
                    "type": "string",
                    "description": "The shell command to execute"
                }
            },
            "required": ["command"]
        }
    },
    {
        "name": "web_search",
        "description": "Search the web for information using DuckDuckGo. Use this when you need current information, facts, documentation, or answers that aren't in local files. Returns a list of search results with titles, URLs, and snippets.",
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The search query to look up on the web"
                },
                "max_results": {
                    "type": "integer",
                    "description": "Maximum number of results to return (default: 5, max: 10)",
                    "default": 5
                }
            },
            "required": ["query"]
        }
    }
]


def read_file(path: str) -> Dict[str, Any]:
    """Read a file and return its contents."""
    try:
        # Handle relative paths
        if not os.path.isabs(path):
            path = os.path.abspath(path)

        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()

        return {
            "success": True,
            "content": content,
            "path": path
        }
    except FileNotFoundError:
        return {
            "success": False,
            "error": f"File not found: {path}"
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Error reading file: {str(e)}"
        }


def write_file(path: str, content: str) -> Dict[str, Any]:
    """Write content to a file (creates new or overwrites existing)."""
    try:
        # Handle relative paths
        if not os.path.isabs(path):
            path = os.path.abspath(path)

        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(path), exist_ok=True)

        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)

        return {
            "success": True,
            "message": f"Successfully wrote to {path}",
            "path": path,
            "bytes_written": len(content.encode('utf-8'))
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Error writing file: {str(e)}"
        }


def edit_file(path: str, old_text: str, new_text: str) -> Dict[str, Any]:
    """Edit a file by replacing old_text with new_text."""
    try:
        # Handle relative paths
        if not os.path.isabs(path):
            path = os.path.abspath(path)

        # Read the file
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Check if old_text exists
        if old_text not in content:
            return {
                "success": False,
                "error": f"Could not find the specified text in {path}. Make sure old_text matches exactly."
            }

        # Replace (only first occurrence)
        new_content = content.replace(old_text, new_text, 1)

        # Write back
        with open(path, 'w', encoding='utf-8') as f:
            f.write(new_content)

        return {
            "success": True,
            "message": f"Successfully edited {path}",
            "path": path
        }
    except FileNotFoundError:
        return {
            "success": False,
            "error": f"File not found: {path}"
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Error editing file: {str(e)}"
        }


def shell_command(command: str) -> Dict[str, Any]:
    """Execute a shell command and return the result."""
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=30  # 30 second timeout
        )

        return {
            "success": result.returncode == 0,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "exit_code": result.returncode,
            "command": command
        }
    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "error": f"Command timed out after 30 seconds: {command}"
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Error executing command: {str(e)}"
        }


def web_search(query: str, max_results: int = 5) -> Dict[str, Any]:
    """Search the web using DuckDuckGo and return results."""
    try:
        # Limit max_results to 10 to avoid overwhelming context
        max_results = min(max_results, 10)

        # Perform search using DuckDuckGo
        ddgs = DDGS()
        results = ddgs.text(query, max_results=max_results)

        # Format results for better readability
        formatted_results = []
        for idx, result in enumerate(results, 1):
            formatted_results.append({
                "position": idx,
                "title": result.get("title", ""),
                "url": result.get("href", ""),
                "snippet": result.get("body", "")
            })

        return {
            "success": True,
            "query": query,
            "results_count": len(formatted_results),
            "results": formatted_results
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Error performing web search: {str(e)}",
            "query": query
        }


# Map tool names to their execution functions
TOOL_FUNCTIONS = {
    "read_file": read_file,
    "write_file": write_file,
    "edit_file": edit_file,
    "shell_command": shell_command,
    "web_search": web_search
}


def execute_tool(tool_name: str, tool_input: Dict[str, Any]) -> Dict[str, Any]:
    """Execute a tool by name with the given input."""
    if tool_name not in TOOL_FUNCTIONS:
        return {
            "success": False,
            "error": f"Unknown tool: {tool_name}"
        }

    tool_func = TOOL_FUNCTIONS[tool_name]

    try:
        result = tool_func(**tool_input)
        return result
    except TypeError as e:
        return {
            "success": False,
            "error": f"Invalid parameters for {tool_name}: {str(e)}"
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Error executing {tool_name}: {str(e)}"
        }
