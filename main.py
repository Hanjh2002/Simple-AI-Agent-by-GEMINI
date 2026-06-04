import os
from dotenv import load_dotenv
from colorama import init, Fore, Style
from agent import GeminiCodingAgent

# Khởi tạo colorama để tự động reset màu sắc trên mọi hệ điều hành (Windows/macOS/Linux)
init(autoreset=True)

def main():
    # 1. Tải các biến môi trường từ file .env (Nạp GEMINI_API_KEY)
    load_dotenv()
    
    if not os.getenv("GEMINI_API_KEY"):
        print(f"{Fore.RED}[❌ LỖI] Không tìm thấy GEMINI_API_KEY trong file .env!{Style.RESET_ALL}")
        print("Vui lòng tạo file .env và thêm dòng: GEMINI_API_KEY=your_key_here")
        return

    print(f"{Fore.GREEN}=================================================={Style.RESET_ALL}")
    print(f"{Fore.GREEN}   🚀 GEMINI CODING AGENT (FROM SCRATCH) IS READY!  {Style.RESET_ALL}")
    print(f"{Fore.GREEN}=================================================={Style.RESET_ALL}")
    print(f"Gõ {Fore.YELLOW}'exit'{Style.RESET_ALL} để thoát chương trình.\n")

    # 2. Khởi tạo Agent
    try:
        agent = GeminiCodingAgent()
    except Exception as e:
        print(f"{Fore.RED}[❌ LỖI] Không thể khởi tạo Agent: {str(e)}{Style.RESET_ALL}")
        return

    # 3. Vòng lặp nhận lệnh từ người dùng
    try:
        while True:
            # Nhận prompt từ bàn phím
            user_input = input(f"{Fore.YELLOW}ai_agent_cli > {Style.RESET_ALL}").strip()

            # Kiểm tra các lệnh thoát
            if user_input.lower() in ['exit', 'quit', '/exit', '/quit']:
                print(f"\n{Fore.LIGHTBLACK_EX}Tạm biệt! Chúc bạn một ngày tốt lành.{Style.RESET_ALL}")
                break

            # Lệnh reset hội thoại
            if user_input.lower() == '/reset':
                agent.reset_conversation()
                print(f"{Fore.LIGHTBLACK_EX}Đã xóa lịch sử hội thoại.{Style.RESET_ALL}")
                continue

            # Lệnh xem lịch sử
            if user_input.lower() == '/history':
                msg_count = agent.get_conversation_length()
                print(f"\n{Fore.CYAN}Thống kê hội thoại:{Style.RESET_ALL}")
                print(f"{Fore.LIGHTBLACK_EX}  - Số tin nhắn trong lịch sử: {msg_count}{Style.RESET_ALL}")
                print(f"{Fore.LIGHTBLACK_EX}  - Dùng '/reset' để xóa lịch sử{Style.RESET_ALL}")
                continue

            # Bỏ qua nếu người dùng ấn Enter mà không gõ gì
            if not user_input:
                print(f"{Fore.LIGHTBLACK_EX}Prompt trống. Nhập một task hoặc gõ 'exit' để thoát.{Style.RESET_ALL}")
                continue

            # Chạy Agent — bắt lỗi riêng để vòng lặp không bị ngắt
            try:
                final_answer = agent.run(user_input)
                print(f"\n{Fore.GREEN}[Gemini Phản Hồi]:{Style.RESET_ALL}\n{final_answer}\n")
                print(f"{Fore.LIGHTBLACK_EX}{'-' * 50}{Style.RESET_ALL}")
            except Exception as e:
                print(f"\n{Fore.RED}[❌ LỖI]: {str(e)}{Style.RESET_ALL}")
                import traceback
                traceback.print_exc()
                print(f"{Fore.LIGHTBLACK_EX}Tiếp tục với task kế tiếp...{Style.RESET_ALL}\n")

    except KeyboardInterrupt:
        print(f"\n\n{Fore.LIGHTBLACK_EX}Chương trình bị ngắt bởi người dùng. Đang thoát...{Style.RESET_ALL}")
    except EOFError:
        print(f"\n\n{Fore.LIGHTBLACK_EX}Tạm biệt!{Style.RESET_ALL}")

if __name__ == "__main__":
    main()
    