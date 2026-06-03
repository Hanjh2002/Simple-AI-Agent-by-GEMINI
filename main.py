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
    while True:
        try:
            # Nhận prompt từ bàn phím
            user_input = input(f"{Fore.YELLOW}ai_agent_cli > {Style.RESET_ALL}").strip()
            
            # Kiểm tra nếu người dùng muốn thoát
            if user_input.lower() == 'exit':
                print(f"\n{Fore.LIGHTBLACK_EX}Tạm biệt! Chúc bạn một ngày tốt lành.{Style.RESET_ALL}")
                break
                
            # Bỏ qua nếu người dùng ấn Enter mà không gõ gì
            if not user_input:
                continue
                
            # Chạy Agent và nhận kết quả cuối cùng
            final_answer = agent.run(user_input)
            
            # In câu trả lời cuối cùng của Agent ra màn hình
            print(f"\n{Fore.GREEN}[Gemini Phản Hồi]:{Style.RESET_ALL}\n{final_answer}\n")
            print(f"{Fore.LIGHTBLACK_EX}--------------------------------------------------{Style.RESET_ALL}")
            
        except KeyboardInterrupt:
            # Xử lý khi bấm Ctrl+C để thoát mượt mà
            print(f"\n\n{Fore.LIGHTBLACK_EX}Chương trình bị ngắt bởi người dùng. Đang thoát...{Style.RESET_ALL}")
            break
        except Exception as e:
            print(f"\n{Fore.RED}[❌ LỖI HỆ THỐNG]: {str(e)}{Style.RESET_ALL}\n")

if __name__ == "__main__":
    main()
    