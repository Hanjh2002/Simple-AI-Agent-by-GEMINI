import os
from google import genai
from google.genai import types
from colorama import Fore, Style
import tools  # Import các công cụ chúng ta vừa viết ở bước trước

class GeminiCodingAgent:
    def __init__(self):
        # 1. Khởi tạo Client của Google GenAI (Tự động lấy GEMINI_API_KEY từ file .env)
        self.client = genai.Client()
        
        # 2. Định nghĩa danh sách các hàm công cụ thuần Python
        self.available_tools = [
            tools.read_file,
            tools.write_file,
            tools.edit_file,
            tools.shell_command,
            tools.web_search
        ]
        
        # 3. Lựa chọn model: gemini-2.5-flash là lựa chọn tối ưu nhất cho Agent 
        # nhờ tốc độ phản hồi cực nhanh, giá free tier tốt và khả năng gọi Tool chuẩn xác.
        self.model_name = "gemini-2.5-flash"
        
        # 4. Tạo cấu hình hệ thống (System Instruction) và tích hợp Tools
        self.config = types.GenerateContentConfig(
            system_instruction=(
                "You are an advanced AI coding assistant. You have access to tools "
                "to interact with the file system, execute terminal commands, and search the web. "
                "Always use these tools when you need to view, create, edit files, or gather information. "
                "Be concise, efficient, and precise in your reasoning."
            ),
            tools=self.available_tools,
            temperature=0.2, # Giữ temperature thấp để Agent suy luận logic ổn định hơn
        )
        
        # 5. Khởi tạo phiên Chat (Phiên này tự động quản lý Lịch sử hội thoại/Bộ nhớ cho chúng tra)
        self.chat = self.client.chats.create(model=self.model_name, config=self.config)

    def run(self, user_prompt: str):
        """Kích hoạt vòng lặp ReAct khi người dùng gửi yêu cầu."""
        print(f"\n{Fore.BLUE}[User]:{Style.RESET_ALL} {user_prompt}")
        
        # Gửi tin nhắn đầu tiên của User vào phiên chat
        response = self.chat.send_message(user_prompt)
        
        # Vòng lặp ReAct (Reason + Act): Lặp liên tục nếu Gemini yêu cầu gọi công cụ
        while response.function_calls:
            for function_call in response.function_calls:
                tool_name = function_call.name
                # Lấy các tham số mà Gemini truyền vào (dưới dạng dictionary)
                tool_args = function_call.args 
                
                print(f"{Fore.CYAN}[Gemini Suy Nghĩ]:{Style.RESET_ALL} Cần sử dụng công cụ {Fore.GREEN}{tool_name}{Style.RESET_ALL} với tham số {tool_args}")
                
                # Bản đồ ánh xạ từ tên hàm (string) sang hàm thực thi thực tế trong tools.py
                tool_result = ""
                try:
                    if tool_name == "read_file":
                        tool_result = tools.read_file(**tool_args)
                    elif tool_name == "write_file":
                        tool_result = tools.write_file(**tool_args)
                    elif tool_name == "edit_file":
                        tool_result = tools.edit_file(**tool_args)
                    elif tool_name == "web_search":
                        tool_result = tools.web_search(**tool_args)
                    elif tool_name == "shell_command":
                        tool_result = tools.shell_command(**tool_args)
                    else:
                        tool_result = f"Error: Tool '{tool_name}' không tồn tại."
                except Exception as e:
                    tool_result = f"Error khi thực thi tool: {str(e)}"
                
                print(f"{Fore.MAGENTA}[Hệ Thống Trả Kết Quả]:{Style.RESET_ALL} Đang gửi kết quả của {tool_name} về cho Gemini...")
                
                # Gửi kết quả (Observation) ngược lại cho Gemini để nó đọc và phân tích tiếp
                response = self.chat.send_message(
                    types.Part.from_function_response(
                        name=tool_name,
                        response={"result": tool_result}
                    )
                )
        
        # Khi vòng lặp kết thúc (Gemini không gọi tool nữa tức là đã giải quyết xong task)
        # Trả về văn bản phản hồi cuối cùng cho người dùng
        return response.text
    