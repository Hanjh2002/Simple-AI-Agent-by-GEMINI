
import os
import subprocess
from colorama import Fore, Style
from duckduckgo_search import DDGS

def read_file(path: str) -> str:
    """Read the contents of a file.

    Args:
        path: The file path to read.
    """
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return f"Error reading file {path}: {str(e)}"

def write_file(path: str, content: str) -> str:
    """Create or overwrite a file with new content.

    Args:
        path: The file path to write to.
        content: The text content to write inside the file.
    """
    try:
        # Tự động tạo thư mục cha nếu chưa có
        os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        return f"Successfully wrote to {path}"
    except Exception as e:
        return f"Error writing file {path}: {str(e)}"

def edit_file(path: str, old_text: str, new_text: str) -> str:
    """Find and replace a specific block of text in a file.

    Args:
        path: The file path to edit.
        old_text: The exact block of text to look for.
        new_text: The new text to replace the old text with.
    """
    try:
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if old_text not in content:
            return f"Error: The exact text block to replace was not found in {path}"
            
        updated_content = content.replace(old_text, new_text)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(updated_content)
        return f"Successfully updated {path}"
    except Exception as e:
        return f"Error editing file {path}: {str(e)}"
    
def append_file(path: str, content: str) -> str:
    """Append text content to the end of an existing file.

    Args:
        path: The file path to append to.
        content: The text content to add at the end of the file.
    """
    try:
        with open(path, 'a', encoding='utf-8') as f:
            f.write("\n" + content)
        return f"Successfully appended new content to {path}"
    except Exception as e:
        return f"Error appending to file {path}: {str(e)}"

def web_search(query: str) -> str:
    """Search the web using DuckDuckGo to get up-to-date information.

    Args:
        query: The search query string.
    """
    try:
        with DDGS() as ddgs:
            results = [r for r in ddgs.text(query, max_results=5)]
            if not results:
                return "No search results found."
            
            formatted_results = []
            for r in results:
                formatted_results.append(f"Title: {r['title']}\nURL: {r['href']}\nSnippet: {r['body']}\n---")
            return "\n".join(formatted_results)
    except Exception as e:
        return f"Error performing web search: {str(e)}"

def shell_command(command: str) -> str:
    """Execute a shell/terminal command safely with human-in-the-loop confirmation.

    Args:
        command: The terminal command to execute (e.g., 'ls', 'pytest').
    """
    # Cơ chế bảo mật Human-in-the-loop: Hỏi ý kiến bạn trước khi chạy lệnh Terminal
    print(f"\n{Fore.YELLOW}[⚠️ BẢO MẬT] Agent muốn chạy lệnh:{Style.RESET_ALL} {Fore.GREEN}{command}{Style.RESET_ALL}")
    choice = input("Bạn có cho phép không? (y/n): ").strip().lower()
    
    if choice != 'y':
        return "Command execution aborted by the user."
        
    try:
        # Chạy lệnh hệ thống và bắt kết quả trả về
        result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=30)
        output = result.stdout
        if result.stderr:
            output += f"\nErrors:\n{result.stderr}"
        return output if output.strip() else "Command executed successfully with no output."
    except subprocess.TimeoutExpired:
        return "Error: Command timed out after 30 seconds."
    except Exception as e:
        return f"Error executing command: {str(e)}"
    