import streamlit as st

import uuid
from shared.sql_executor import ChatHistory, execute_sql_to_df
from shared.messages import ChatbotMessage, MESSAGE_TYPE
from shared.chat_model import llm_chat_base
import os
import yaml

from implements.P03_router import route_question, ROUTER_QUESTION
from implements.P04_preprocessor import preprocess_question
from implements.P05_context_retriever import retrieve_context


# =========================
# Load prompts từ file YAML
# =========================
prompt_file = os.path.join(os.path.dirname(__file__), "implements", "P06_prompt.yml")
with open(prompt_file, 'r', encoding='utf-8') as f:
    PROMPTS = yaml.safe_load(f)


# =========================
# Page config
# =========================
st.set_page_config(
    page_title="LLM SQL Chatbot Demo",
    layout="wide"
)


# =========================
# DB config
# =========================
DB_PATH = os.path.join(os.path.dirname(__file__), "db", "demo.db")

# =========================
# Session state init
# =========================
if "active_conversation_id" not in st.session_state:
    st.session_state.active_conversation_id = None
if "last_processed_input" not in st.session_state:
    st.session_state.last_processed_input = None


# =========================
# Hàm hỗ trợ quản lý conversation
# =========================
def create_new_conversation():
    """Tạo conversation mới với title tự động tăng"""
    # Nếu đã có conversation active và conversation đó chưa có message user thì không tạo mới
    cid = st.session_state.active_conversation_id
    if cid:
        chat = ChatHistory(DB_PATH, cid)
        messages = chat.get()
        # Nếu chỉ có message hệ thống (hoặc rỗng), không tạo mới
        user_msgs = [m for m in messages if m.type == MESSAGE_TYPE.USER]
        if not user_msgs:
            # Đã có conversation rỗng, chỉ chuyển sang nó
            return
    
    # Tạo mới conversation
    conv_id = str(uuid.uuid4())
    
    # Tính số thứ tự conversations đã tạo (bao gồm cả đã xóa)
    # Lấy max số từ các title hiện có
    all_convs = ChatHistory.list_conversations(DB_PATH)
    max_num = 0
    for existing_cid in all_convs:
        existing_title = ChatHistory.get_conversation_title(DB_PATH, existing_cid)
        if existing_title and existing_title.startswith("Conversation "):
            try:
                num = int(existing_title.replace("Conversation ", ""))
                max_num = max(max_num, num)
            except ValueError:
                pass
    
    title = f"Conversation {max_num + 1}"
    
    # Tạo conversation trong database
    ChatHistory.create_conversation(DB_PATH, conv_id, title)
    st.session_state.active_conversation_id = conv_id


def delete_conversation(conv_id):
    ChatHistory.delete_conversation(DB_PATH, conv_id)
    if st.session_state.active_conversation_id == conv_id:
        # Chọn conversation khác nếu có, nếu không thì None
        all_convs = ChatHistory.list_conversations(DB_PATH)
        st.session_state.active_conversation_id = all_convs[0] if all_convs else None


def get_active_conversation():
    cid = st.session_state.active_conversation_id
    if cid:
        # Kiểm tra xem conversation có tồn tại không
        all_convs = ChatHistory.list_conversations(DB_PATH)
        if cid in all_convs:
            return ChatHistory(DB_PATH, cid)
        else:
            # Conversation đã bị xóa, reset về None
            st.session_state.active_conversation_id = None
    return None


# =========================
# Hàm hỗ trợ chatbot
# =========================
def format_table_context(tables: list) -> str:
    """Format danh sách TableDescription thành chuỗi ngữ cảnh"""
    context_parts = []
    for table in tables:
        table_info = f"> Bảng `{table.name}`\n"
        table_info += f"  - Mô tả bảng: {table.description}\n"
        table_info += f"  - Danh sách cột:\n"
        
        columns_info = []
        for col in table.table_columns:
            columns_info.append(f"    + Cột `{col.column_name}`: {col.column_description}")
        table_info += "\n".join(columns_info)
        
        context_parts.append(table_info)
    
    return "\n\n".join(context_parts)


def stream_llm_response(prompt: str):
    """Generator để streaming response từ LLM"""
    msg = llm_chat_base._to_langchain_prompt(prompt)
    
    for chunk in llm_chat_base.model.stream(msg):
        if hasattr(chunk, 'content') and chunk.content:
            yield chunk.content

# =========================
# Định nghĩa luồng chatbot
# =========================
def run_llm_pipeline(user_message: str, conversation: ChatHistory, status_placeholder):
    """
    Pipeline xử lý chatbot:
    1. Preprocess question
    2. Route question
    3. Nếu NON_QUERY: trả lời trực tiếp (streaming)
    4. Nếu QUERY: retrieve context -> generate SQL -> execute -> generate answer (streaming)
    
    Returns: tuple (generator, debug_info)
    """
    debug_info = {
        "processed_question": "",
        "route": "",
        "relevant_table": "",
        "sql_query": "",
        "sql_result": ""
    }
    
    # Lấy lịch sử chat để preprocess
    chat_history = conversation.get()[:-1]
    
    # ===== Bước 1: Chuẩn hóa câu hỏi =====
    
    with status_placeholder.spinner("🔍 Đang chuẩn hóa câu hỏi..."):
        processed_question = preprocess_question(user_message, chat_history)
    
    debug_info["processed_question"] = processed_question
    
    # ===== Hết Bước 1 =====
    
    # ===== Bước 2: Phân định luồng =====
    
    with status_placeholder.spinner("🚦 Đang phân định luồng xử lý..."):
        route = route_question(processed_question)
    
    debug_info["route"] = route.value
    
    # ===== Hết Bước 2 =====
    
    if route == ROUTER_QUESTION.NON_QUERY:
        # ===== Luồng NON_QUERY =====
        
        status_placeholder.empty()
        
        prompt = f"""
            Bạn là trợ lý ảo hỗ trợ người dùng.

            ### Câu hỏi người dùng:

            {processed_question}

            ### Yêu cầu:

            Hãy trả lời câu hỏi của người dùng một cách thân thiện và hữu ích."""
        
        return stream_llm_response(prompt), debug_info
    
        # ===== Kết thúc phân luồng NON_QUERY =====
    else:
        # ===== Luồng QUERY =====
        
        # ===== Bước 3: Truy vấn tương đồng =====
        with status_placeholder.spinner("📊 Đang truy xuất ngữ cảnh cơ sở dữ liệu..."):
            tables = retrieve_context(processed_question, k=4)
            context = format_table_context(tables)
        
        debug_info["relevant_table"] = [t.name for t in tables]
        
        # ===== Hết Bước 3 =====
        
        # ===== Bước 4: Tạo SQL =====
        with status_placeholder.spinner("🔨 Đang tạo truy vấn SQL..."):
            sql_prompt = PROMPTS['generate_sql']
            prompt = f"""
                {sql_prompt}

                ### Schema bảng/cột truy vấn:

                {context}

                ### Câu hỏi người dùng:

                {processed_question}

                ### Yêu cầu đầu ra:

                Chỉ trả về câu truy vấn SQL, không kèm theo giải thích."""
            sql_query = llm_chat_base.generate(prompt).strip()
            
            # Loại bỏ markdown code block nếu có
            if sql_query.startswith("```"):
                lines = sql_query.split('\n')
                sql_query = '\n'.join(lines[1:-1]) if len(lines) > 2 else sql_query
            sql_query = sql_query.replace("```sql", "").replace("```", "").strip()
            
            debug_info["sql_query"] = sql_query
        
        # ===== Hết Bước 4 =====
        
        # ===== Bước 5: Thực thi SQL =====
        with status_placeholder.spinner("⚡ Đang thực thi truy vấn..."):
            try:
                df = execute_sql_to_df(sql_query, DB_PATH)
                
                if not df.empty:
                    result_str = df.to_json(
                        orient="records", force_ascii=False,
                        lines=True, indent=2
                    )
                else:
                    result_str = "Kết quả trả về rỗng."
                
                debug_info["sql_result"] = result_str
            except Exception as e:
                status_placeholder.error(f"❌ Lỗi thực thi SQL: {str(e)}")
                
                debug_info["sql_result"] = f"Error: {str(e)}"
                
                return iter([f"❌ Lỗi khi thực thi SQL: {str(e)}\n\nSQL: {sql_query}"]), debug_info
        
        # ===== Hết Bước 5 =====
        
        # ===== Bước 6: Tạo câu trả lời (streaming) =====
        
        status_placeholder.empty()
        answer_prompt = PROMPTS['generate_answer']
        prompt = f"""
            {answer_prompt}

            ### Câu hỏi người dùng:

            {processed_question}

            ### Truy vấn SQL đã thực thi:

            {sql_query}

            ### Kết quả truy vấn:

            {result_str}

            ### Yêu cầu đầu ra

            Hãy tạo câu trả lời tự nhiên dựa trên kết quả trên."""
        
        return stream_llm_response(prompt), debug_info
        
        # ===== Kết thúc phân luồng QUERY =====


# =========================
# UI: Sidebar
# =========================
with st.sidebar:
    st.title("💬 Chatbot Demo")

    if st.button("➕ Cuộc trò chuyện mới"):
        create_new_conversation()

    st.divider()

    for cid in ChatHistory.list_conversations(DB_PATH):
        # Lấy tiêu đề từ bảng conversations
        title = ChatHistory.get_conversation_title(DB_PATH, cid)
        if not title:
            title = f"Conversation {cid[:8]}"
        
        # Kiểm tra xem đây có phải conversation đang active không
        is_active = (cid == st.session_state.active_conversation_id)
        
        col1, col2 = st.columns([4, 1])
        with col1:
            # Sử dụng type khác nhau để highlight active conversation
            button_type = "primary" if is_active else "secondary"
            if st.button(title, key=f"select_{cid}", type=button_type, use_container_width=True):
                st.session_state.active_conversation_id = cid
                st.rerun()
        with col2:
            if st.button("🗑️", key=f"delete_{cid}"):
                delete_conversation(cid)
                st.rerun()


# =========================
# UI: Main chat area
# =========================
st.title("📊 Chatbot truy vấn dữ liệu (Demo)")


chat = get_active_conversation()

# Hiển thị lịch sử chat nếu có conversation active
if chat is not None:
    for msg in chat.get():
        role = "user" if msg.type == MESSAGE_TYPE.USER else ("assistant" if msg.type == MESSAGE_TYPE.ASSISTANT else "system")
        if role == "system":
            continue
        with st.chat_message(role):
            st.markdown(msg.content)
            # Hiển thị debug info cho assistant messages
            if role == "assistant" and msg.debug:
                with st.expander("🔍 Thông tin debug", expanded=False):
                    if msg.debug.get("processed_question"):
                        st.write("**Câu hỏi chuẩn hóa:**")
                        st.code(msg.debug["processed_question"], language="text")
                    
                    if msg.debug.get("route"):
                        st.write("**Luồng xử lý:**")
                        st.code(msg.debug["route"], language="text")
                    
                    if msg.debug.get("relevant_table"):
                        st.write("**Bảng liên quan:**")
                        st.code(msg.debug["relevant_table"], language="sql")
                    
                    if msg.debug.get("sql_query"):
                        st.write("**Truy vấn SQL:**")
                        st.code(msg.debug["sql_query"], language="sql")
                    
                    if msg.debug.get("sql_result"):
                        st.write("**Kết quả truy vấn:**")
                        st.code(msg.debug["sql_result"], language="text")
else:
    st.info("💬 Nhấn nút '➕ Cuộc trò chuyện mới' ở sidebar để bắt đầu")


# =========================
# UI: Chat input
# =========================
if chat is not None:
    user_input = st.chat_input("Nhập câu hỏi...")

    if user_input and user_input != st.session_state.last_processed_input:
        # Đánh dấu input đã được xử lý để tránh duplicate
        st.session_state.last_processed_input = user_input
        
        # Lưu message user vào db
        chat.add(ChatbotMessage(type=MESSAGE_TYPE.USER, content=user_input))

        # Hiển thị message user
        with st.chat_message("user"):
            st.markdown(user_input)

        # Gọi pipeline LLM với streaming
        with st.chat_message("assistant"):
            # Tạo placeholder cho status và message
            status_placeholder = st.empty()
            message_placeholder = st.empty()
            full_response = ""
            
            # Chạy pipeline với status placeholder
            response_generator, debug_info = run_llm_pipeline(
                user_message=user_input,
                conversation=chat,
                status_placeholder=status_placeholder
            )
            
            # Stream response
            for chunk in response_generator:
                full_response += chunk
                message_placeholder.markdown(full_response + "▌")
            
            # Hiển thị response hoàn chỉnh
            message_placeholder.markdown(full_response)
            
            # Hiển thị debug info
            if debug_info:
                with st.expander("🔍 Thông tin debug", expanded=False):
                    if debug_info.get("processed_question"):
                        st.write("**Câu hỏi chuẩn hóa:**")
                        st.code(debug_info["processed_question"], language="text")
                    
                    if debug_info.get("route"):
                        st.write("**Luồng xử lý:**")
                        st.code(debug_info["route"], language="text")
                    
                    if debug_info.get("sql_query"):
                        st.write("**Truy vấn SQL:**")
                        st.code(debug_info["sql_query"], language="sql")
                    
                    if debug_info.get("sql_result"):
                        st.write("**Kết quả truy vấn:**")
                        st.code(debug_info["sql_result"], language="text")

        # Lưu message assistant vào db với debug info
        chat.add(ChatbotMessage(type=MESSAGE_TYPE.ASSISTANT, content=full_response, debug=debug_info))
        
        # Reset state
        st.session_state.last_processed_input = None
        st.rerun()