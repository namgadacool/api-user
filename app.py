import os
import streamlit as st
import anthropic
from dotenv import load_dotenv

# 1. Tải các biến môi trường từ file .env lên hệ thống
load_dotenv()

# Lấy API Key
api_key = os.getenv("ANTHROPIC_API_KEY")

# 2. Cấu hình giao diện
st.set_page_config(page_title="Claude Web App", page_icon="🤖")
st.title("Trợ lý AI với Claude API")

# Kiểm tra xem đã có API Key trong file .env chưa
if not api_key:
    st.error("Không tìm thấy ANTHROPIC_API_KEY trong file .env. Vui lòng kiểm tra lại!")
    st.stop() # Dừng việc chạy app lại nếu thiếu key

# 3. Khởi tạo bộ nhớ lưu trữ tin nhắn
if "messages" not in st.session_state:
    st.session_state.messages = []

# Hiển thị lại các tin nhắn cũ
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 4. Xử lý tin nhắn mới
if prompt := st.chat_input("Bạn muốn hỏi Claude điều gì?"):
    # Cập nhật tin nhắn người dùng
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
        
    # Gọi API
    client = anthropic.Anthropic(api_key=api_key)
    with st.chat_message("assistant"):
        with st.spinner("Đang xử lý..."):
            try:
                response = client.messages.create(
                    model="claude-3-5-sonnet-20241022",
                    max_tokens=1024,
                    messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
                )
                reply_text = response.content[0].text
                st.markdown(reply_text)
                
                # Lưu lại lịch sử
                st.session_state.messages.append({"role": "assistant", "content": reply_text})
            except Exception as e:
                st.error(f"Có lỗi xảy ra: {e}")