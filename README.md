# 🚀 Building Gemini Code from Scratch: A Simple Journey into AI Agents

> **Chuyển kiến trúc sang Gemini:** Dự án này lấy cảm hứng từ bài viết trên Medium của tác giả JBY về việc tự xây một AI Coding Assistant (kiểu Claude Code, Cursor) chỉ với ~300 dòng Python thuần, không cần các framework cồng kềnh như LangChain, LangGraph hay CrewAI.
>
> Phiên bản này được viết lại hoàn toàn cho **Google Gemini API** (dùng được với gói Free Tier của Google AI Studio), tận dụng khả năng **Automatic Function Calling** của SDK `google-genai` để code gọn hơn đáng kể so với bản gốc viết cho Claude.

---

## 📌 Câu hỏi lớn: Tại sao tự code từ đầu mà không dùng Framework?

Khi mới nghiên cứu AI Agent, ta rất dễ choáng ngợp bởi tài liệu của LangChain hay CrewAI — các lớp trừu tượng (abstraction) phức tạp khiến việc học trở nên nặng nề. Đúng như một bài viết công nghệ năm 2025 đã chỉ ra:

> *"Companies often adopt 'unearned complexity' by deciding on LangChain or multi-agentic solutions without experimenting enough to understand if they actually need that complexity."*
> *(Các công ty thường gánh 'sự phức tạp không đáng có' khi vội chọn giải pháp đa agent hoặc LangChain mà chưa thử nghiệm đủ để biết mình có thực sự cần nó hay không.)*

Dự án chọn hướng ngược lại: **xây thứ đơn giản nhất có thể chạy được, chỉ thêm phức tạp khi thực sự cần.** Kết quả là một Agent gọn gàng trong ~350 dòng qua 4 file, không lớp trừu tượng, không phụ thuộc framework, dễ debug và dễ kiểm soát.

---

## 🛠️ Những gì đã xây dựng

1. **Lớp công cụ (Tools Layer):** 5 công cụ đang được đăng ký với Agent — `read_file` (đọc file), `write_file` (tạo/ghi đè file), `edit_file` (tìm & thay khối chữ), `shell_command` (chạy lệnh terminal), `web_search` (tìm web qua DuckDuckGo).
2. **Vòng lặp ReAct (Reason + Act):** Agent tự lặp chuỗi *Suy nghĩ → Hành động → Quan sát kết quả* cho đến khi hoàn thành tác vụ. Ở bản này, vòng lặp chủ yếu do SDK `google-genai` tự đảm nhiệm thông qua Automatic Function Calling (xem mục Kiến trúc bên dưới).
3. **Bộ nhớ hội thoại tự động:** Dùng `client.chats.create(...)` để SDK tự giữ toàn bộ ngữ cảnh hội thoại, không phải quản lý mảng lịch sử thủ công.
4. **Bảo mật Human-in-the-loop:** `shell_command` luôn hỏi xác nhận (y/n) trước khi chạy lệnh terminal.
5. **Giao diện CLI có màu:** Dùng `colorama` để phân biệt rõ các bước tư duy của Agent.

---

## 💎 Khác biệt so với bản gốc viết cho Claude

* **Bỏ hoàn toàn JSON Schema viết tay.** Bản Claude phải tự khai báo mảng JSON dài để mô tả từng hàm cho API. SDK `google-genai` thông minh hơn: nó tự đọc trực tiếp hàm Python thuần, phân tích type hint (`path: str`) và docstring để tự sinh schema công cụ. Nhờ vậy file `tools.py` ngắn và sạch hơn nhiều.
* **Bộ nhớ hội thoại do SDK tự quản.** Bản gốc phải tự `append` từng message vào `conversation_history`. Bản này để `chats.create()` lo, giảm code và giảm rủi ro quên cập nhật lịch sử.
* **Tận dụng Automatic Function Calling (AFC).** Khi truyền hàm Python làm tool, SDK tự gọi tool và lặp vòng ReAct hộ (mặc định tối đa 10 lượt gọi), nên logic điều phối ở tầng ứng dụng được tối giản.

---

## 🏗️ Kiến trúc: vòng lặp ReAct hoạt động ra sao

Điểm cần lưu ý: vì truyền **hàm Python (callable)** vào `tools`, SDK `google-genai` **mặc định bật Automatic Function Calling**. Nghĩa là khi gọi `chat.send_message(prompt)`, chính SDK đã tự thực thi tool và lặp vòng ReAct trước khi trả `response` cuối cùng. Tool (kể cả phần hỏi `y/n` trong `shell_command`) vẫn được gọi đúng — nhưng bởi AFC, chứ không phải bởi vòng lặp thủ công trong `agent.py`.

Nếu muốn **tự điều khiển** vòng lặp (để chặn/log từng bước), cần tắt AFC bằng cách thêm vào `config`:

```python
automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=True)
```

---

## 📂 Cấu trúc thư mục

```text
├── .env                  # Lưu GEMINI_API_KEY (không commit lên git)
├── requirements.txt      # Danh sách thư viện phụ thuộc
├── tools.py              # Định nghĩa các hàm công cụ thuần Python
├── agent.py              # Khởi tạo Agent & vòng lặp ReAct của Gemini
└── main.py               # Giao diện dòng lệnh (CLI)
```

---

## ⚙️ Cài đặt & chạy

```bash
# 1. Clone repo
git clone https://github.com/Hanjh2002/Simple-AI-Agent-by-GEMINI.git
cd Simple-AI-Agent-by-GEMINI

# 2. Cài thư viện
pip install -r requirements.txt

# 3. Tạo file .env và thêm API key (lấy free tại https://aistudio.google.com)
echo "GEMINI_API_KEY=your_key_here" > .env

# 4. Chạy Agent
python main.py
```

Gõ `exit` để thoát chương trình.

---

## 🚧 Hạn chế hiện tại & lộ trình

Những điểm dưới đây **chưa có trong code**, đang để mở để cải tiến tiếp:

* **`write_file` và `edit_file` chưa hỏi xác nhận.** Hiện chỉ `shell_command` có chốt y/n; agent có thể tạo/ghi đè file mà không hỏi. Dự kiến thêm xác nhận cho cả hai.
* **`edit_file` thay tất cả occurrence.** Đang dùng `str.replace` không giới hạn — nên đổi sang thay đúng lần đầu (`count=1`) để tránh sửa nhầm.
* **Công cụ `append_file`.** Đã viết trong `tools.py` nhưng **chưa được đăng ký** vào `available_tools`, nên Agent chưa dùng được. Cần thêm vào danh sách tool.
* **Web search vẫn dùng DuckDuckGo.** Dễ dính lỗi `Ratelimit`/`503`. Định hướng: chuyển sang công cụ Google Search tích hợp sẵn của Gemini.
* **Chưa xử lý SSL/proxy mạng doanh nghiệp.** Nếu chạy sau tường lửa công ty có thể gặp `SSL: CERTIFICATE_VERIFY_FAILED`; dự kiến bổ sung xử lý chứng chỉ.
* **Thư viện `duckduckgo-search` đã đổi tên thành `ddgs`.** Nên cập nhật import và `requirements.txt`.

---

> Dự án phục vụ mục đích học tập — hiểu cách một coding agent hoạt động từ gốc, không phải để thay thế các công cụ production như Claude Code hay Cursor.
