import streamlit as st
import uuid
from datetime import datetime

# =========================
# Page config
# =========================
st.set_page_config(
    page_title="LLM SQL Chatbot Demo",
    layout="wide"
)

# =========================
# Session state init
# =========================
if "conversations" not in st.session_state:
    st.session_state.conversations = {}

if "active_conversation_id" not in st.session_state:
    st.session_state.active_conversation_id = None


# =========================
# Conversation helpers
# =========================
def create_new_conversation():
    conv_id = str(uuid.uuid4())
    st.session_state.conversations[conv_id] = {
        "id": conv_id,
        "title": f"Conversation {len(st.session_state.conversations) + 1}",
        "created_at": datetime.now(),
        "messages": []
    }
    st.session_state.active_conversation_id = conv_id


def delete_conversation(conv_id):
    if conv_id in st.session_state.conversations:
        del st.session_state.conversations[conv_id]
        if st.session_state.active_conversation_id == conv_id:
            st.session_state.active_conversation_id = None


def get_active_conversation():
    cid = st.session_state.active_conversation_id
    if cid:
        return st.session_state.conversations.get(cid)
    return None


# =========================
# LLM pipeline placeholder
# =========================
def run_llm_pipeline(user_message: str, conversation: dict) -> str:
    """
    Placeholder cho pipeline tất định:
    - chuẩn hóa câu hỏi
    - truy xuất metadata
    - sinh SQL
    - execute SQL
    - sinh câu trả lời
    """
    # TODO: implement sau
    return f"[LLM trả lời giả lập] Bạn vừa hỏi: {user_message}"


# =========================
# Sidebar: conversation list
# =========================
with st.sidebar:
    st.title("💬 Chatbot Demo")

    if st.button("➕ Cuộc trò chuyện mới"):
        create_new_conversation()

    st.divider()

    for cid, conv in st.session_state.conversations.items():
        col1, col2 = st.columns([4, 1])

        with col1:
            if st.button(conv["title"], key=f"select_{cid}"):
                st.session_state.active_conversation_id = cid

        with col2:
            if st.button("🗑️", key=f"delete_{cid}"):
                delete_conversation(cid)
                st.rerun()


# =========================
# Main chat area
# =========================
st.title("📊 Chatbot truy vấn dữ liệu (Demo)")

conversation = get_active_conversation()

if conversation is None:
    st.info("Hãy tạo hoặc chọn một cuộc trò chuyện để bắt đầu.")
    st.stop()


# Hiển thị lịch sử chat
for msg in conversation["messages"]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])


# =========================
# Chat input
# =========================
user_input = st.chat_input("Nhập câu hỏi...")

if user_input:
    # Lưu message user
    conversation["messages"].append({
        "role": "user",
        "content": user_input
    })

    with st.chat_message("user"):
        st.markdown(user_input)

    # Gọi pipeline LLM
    with st.chat_message("assistant"):
        with st.spinner("Đang xử lý..."):
            assistant_reply = run_llm_pipeline(
                user_message=user_input,
                conversation=conversation
            )
            st.markdown(assistant_reply)

    # Lưu message assistant
    conversation["messages"].append({
        "role": "assistant",
        "content": assistant_reply
    })