"""
UI utilities for colored and formatted terminal output.
"""

from colorama import Fore, Back, Style, init

# Initialize colorama for cross-platform support
init(autoreset=True)


# Color functions
def success(text: str) -> str:
    """Green text for success messages."""
    return f"{Fore.GREEN}{text}{Style.RESET_ALL}"


def error(text: str) -> str:
    """Red text for error messages."""
    return f"{Fore.RED}{text}{Style.RESET_ALL}"


def warning(text: str) -> str:
    """Yellow text for warnings."""
    return f"{Fore.YELLOW}{text}{Style.RESET_ALL}"


def info(text: str) -> str:
    """Cyan text for informational messages."""
    return f"{Fore.CYAN}{text}{Style.RESET_ALL}"


def tool_color(text: str) -> str:
    """Magenta text for tool-related messages."""
    return f"{Fore.MAGENTA}{text}{Style.RESET_ALL}"


def dim(text: str) -> str:
    """Dimmed text for less important info."""
    return f"{Style.DIM}{text}{Style.RESET_ALL}"


# Formatting functions
def bold(text: str) -> str:
    """Bold text."""
    return f"{Style.BRIGHT}{text}{Style.RESET_ALL}"


def header(text: str, width: int = 60) -> str:
    """Create a formatted header with separator."""
    separator = "=" * width
    return f"{bold(info(separator))}\n{bold(info(text))}\n{bold(info(separator))}"


def subheader(text: str) -> str:
    """Create a subheader."""
    return bold(text)


# Symbol replacements (no emojis)
CHECKMARK = success("[OK]")
CROSS = error("[X]")
WARNING_SYMBOL = warning("[!]")
INFO_SYMBOL = info("[i]")
ARROW = "->"


# Convenience print functions
def print_success(message: str):
    """Print a success message."""
    print(f"{CHECKMARK} {message}")


def print_error(message: str):
    """Print an error message."""
    print(f"{CROSS} {message}")


def print_warning(message: str):
    """Print a warning message."""
    print(f"{WARNING_SYMBOL} {message}")


def print_info(message: str):
    """Print an info message."""
    print(f"{INFO_SYMBOL} {message}")


def print_header(text: str, width: int = 60):
    """Print a formatted header."""
    print(header(text, width))


def print_subheader(text: str):
    """Print a subheader."""
    print(subheader(text))
