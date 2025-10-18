# Simple AI Coding Agent

A minimal implementation of an AI coding agent inspired by Claude Code and Gemini CLI. This is a learning project to understand how AI coding agents work.

## What It Does

This agent uses Anthropic's Claude API with a **ReAct (Reason + Act) loop** to help you with coding tasks. It can:

- **Read files** - Understand your existing codebase
- **Write files** - Create new files from scratch
- **Edit files** - Make targeted changes to existing files
- **Execute shell commands** - Run tests, install packages, etc.

## Architecture

The project consists of three main components:

1. **tools.py** - Defines the 4 tools (read, write, edit, shell) with JSON schemas for Claude
2. **agent.py** - Implements the ReAct loop that calls Claude API and executes tools iteratively
3. **main.py** - Simple CLI interface for user interaction

### How the ReAct Loop Works

```
User Prompt
    ↓
[Claude thinks and decides what to do]
    ↓
Does Claude want to use a tool?
    ├─ YES → Execute tool → Add result to conversation → Loop back to Claude
    └─ NO  → Return final answer to user
```

Claude iteratively uses tools until it completes the task or reaches max iterations (15).

## Setup

### Prerequisites

- Python 3.8+
- Anthropic API key (get one at https://console.anthropic.com/)

### Installation

1. Clone or download this repository

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file with your API key:
```bash
echo "ANTHROPIC_API_KEY=your_api_key_here" > .env
```

## Usage

Run the agent:

```bash
python main.py
```

You'll be prompted to enter your coding task. For example:

```
> Create a Python script that calculates the fibonacci sequence up to n terms
```

The agent will:
1. Think about the task
2. Use tools to create the file
3. Optionally test it
4. Report back to you

### Example Tasks

- "Create a simple calculator in Python"
- "Add error handling to the existing calculator.py file"
- "Write unit tests for my fibonacci.py script"
- "Create a README for this project"

## Tool Confirmations

For safety, you'll be asked to confirm before the agent:
- Writes or edits files
- Executes shell commands

Read-only operations (reading files) run automatically.

## Project Structure

```
.
├── .env                 # API key (not in git)
├── .gitignore          # Git ignore rules
├── README.md           # This file
├── requirements.txt    # Python dependencies
├── tools.py           # Tool definitions and execution
├── agent.py           # ReAct loop implementation
└── main.py            # CLI interface
```

## How It Compares to Production Tools

This is a **simplified learning project**. Production tools like Claude Code or Gemini CLI have:

- Multi-file operations
- Git integration
- MCP (Model Context Protocol) support
- Sophisticated permission systems
- Session management
- Error recovery
- Code indexing
- Much more...

This project has the **core concept** in ~300 lines of Python.

## Technical Details

- **Model**: Claude 3.5 Sonnet (claude-3-5-sonnet-20241022)
- **API**: Anthropic Messages API with tool use
- **Max iterations**: 15 (prevents infinite loops)
- **Tool timeout**: 30 seconds for shell commands

## Extending the Agent

Want to add more tools? Edit `tools.py`:

1. Add a new tool schema to `TOOL_SCHEMAS`
2. Implement the tool function
3. Add it to `TOOL_FUNCTIONS` mapping

The agent will automatically use your new tool!

## Troubleshooting

**API key error**: Make sure `.env` exists and contains `ANTHROPIC_API_KEY=...`

**Tool execution fails**: Check file paths are correct and you have appropriate permissions

**Max iterations reached**: The task might be too complex or unclear. Try breaking it into smaller tasks.

## Learn More

- [Anthropic Tool Use Documentation](https://docs.anthropic.com/en/docs/tool-use)
- [Gemini CLI Architecture](https://github.com/google-gemini/gemini-cli/blob/main/docs/architecture.md)
- [ReAct Pattern Paper](https://arxiv.org/abs/2210.03629)

## License

This is a learning project - use it however you want!
