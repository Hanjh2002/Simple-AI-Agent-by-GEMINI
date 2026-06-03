# 🚀 Building Gemini Code from Scratch: A Simple Journey into AI Agents

> **Bản dịch chuyển kiến trúc:** Dự án này được lấy cảm hứng và cải tiến hoàn toàn từ bài viết nổi tiếng trên Medium của tác giả JBY về việc tự xây dựng một AI Coding Assistant (như Claude Code, Cursor) chỉ với ~300 dòng code Python thuần mà không cần dùng đến các framework cồng kềnh như LangChain, LangGraph hay CrewAI. 
> 
> Phiên bản này đã được tối ưu hóa 100% sang **Google Gemini API (Gói Free Tier từ Google AI Studio)**, đồng thời giải quyết triệt để các lỗi kết nối mạng doanh nghiệp (SSL Proxy Interception) và lỗi giới hạn lượt gọi của các thư viện cào web miễn phí.

---

## 📌 Câu hỏi lớn: Tại sao lại tự code từ đầu (From Scratch) mà không dùng Framework?

Khi bắt đầu nghiên cứu về AI Agent, chúng ta rất dễ bị choáng ngợp bởi tài liệu của LangChain hay CrewAI. Các khái niệm trừu tượng (Abstractions) quá phức tạp khiến việc học trở nên nặng nề. Đúng như một bài báo công nghệ năm 2025 đã chỉ ra:

> *"Companies often adopt 'unearned complexity' by deciding on LangChain or multi-agentic solutions without experimenting enough to understand if they actually need that complexity."*
> *(Các công ty thường gánh chịu 'sự phức tạp không đáng có' khi vội vã chọn giải pháp đa agent hoặc LangChain mà chưa thử nghiệm đủ để biết mình có thực sự cần nó hay không).*

Dự án này chọn một cách tiếp cận khác: **Xây dựng thứ đơn giản nhất có thể hoạt động, và chỉ thêm sự phức tạp khi thực sự cần thiết.** Kết quả là chúng ta tạo ra một Agent mạnh mẽ trong ~300 dòng code qua 4 file, không lớp trừu tượng, không phụ thuộc framework, cực kỳ dễ debug và kiểm soát.

---

## 🛠️ Những gì chúng ta đã xây dựng

Hệ thống mã nguồn này sở hữu đầy đủ các thành phần tiêu chuẩn của một Agent công nghiệp:

1. **Hệ thống 5 công cụ (Tools Layer):** Đọc file, tạo file, sửa đổi khối chữ, ghi nối vào cuối file, và thực thi lệnh Terminal cục bộ.
2. **Vòng lặp ReAct (Reason + Act):** Mô hình tư duy chuẩn ngành giúp Agent tự trị lặp lại chuỗi hành động: *Suy nghĩ (Think) ➔ Hành động (Act) ➔ Quan sát kết quả (Observe)* cho đến khi hoàn thành tác vụ.
3. **Bộ nhớ hội thoại tự động (Conversation Memory):** Duy trì toàn bộ ngữ cảnh giúp Agent nhớ được mình đã làm gì ở các bước trước đó.
4. **Bảo mật Human-in-the-Loop:** Cơ chế chặn và hỏi ý kiến người dùng (y/n) trước khi chạy các lệnh Terminal nguy hiểm.
5. **Giao diện CLI thân thiện:** Hiển thị màu sắc (nhờ `colorama`) giúp phân biệt rõ ràng các bước tư duy của AI.

---

## 💎 Các điểm cải tiến vượt trội so với phiên bản Claude gốc

* **Lược bỏ hoàn toàn JSON Schema cồng kềnh:** Ở phiên bản viết cho Claude, tác giả phải tự viết các mảng JSON dài dòng để giải thích cấu trúc hàm cho API. Với SDK `google-genai` mới, Gemini cực kỳ thông minh: Nó tự đọc trực tiếp hàm Python thuần, tự phân tích kiểu dữ liệu (`path: str`) và chuỗi tài liệu (`docstring`) để tự biến thành công cụ của nó.
* **Tích hợp Google Search gốc:** Bản gốc dùng thư viện cào web DuckDuckGo rất dễ bị dính lỗi mạng `503 Service Unavailable` hoặc `Ratelimit` (đặc biệt khi chạy trong mạng công ty chung IP). Chúng ta đã nâng cấp nhúng thẳng công cụ **Google Search chính chủ** của Gemini vào cấu hình. Tốc độ tìm kiếm nhanh gấp bội, thông tin chính xác và hoàn toàn miễn phí.
* **Vá lỗi SSL mạng doanh nghiệp:** File khởi chạy được tích hợp module xử lý chứng chỉ bảo mật, giúp Python vượt qua các lớp tường lửa/proxy giám sát của công ty vốn hay gây ra lỗi `[SSL: CERTIFICATE_VERIFY_FAILED]`.
* **Công cụ Ghi nối (`append_file`):** Giải quyết triệt để việc Agent đoán mò chuỗi chữ cũ khi bạn yêu cầu chèn thêm thông tin vào file có sẵn.

---

## 📂 Cấu trúc thư mục dự án

```text
├── .env                  # Lưu trữ GEMINI_API_KEY bảo mật
├── requirements.txt      # Danh sách thư viện phụ thuộc
├── tools.py              # Định nghĩa các hàm Python công cụ thuần túy
├── agent.py              # Trái tim điều khiển vòng lặp ReAct của Gemini
└── main.py               # Giao diện dòng lệnh CLI & Trình vá lỗi SSL mạng