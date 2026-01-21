from langchain_core.prompts import ChatPromptTemplate
from shared.chat_model import llm_chat_base
from shared.constants import IDENTITY_PROMPT

def preprocess_question(question: str, chat_history: list[dict] | None = None) -> str:
    """
    Chuẩn hóa câu hỏi người dùng.
    
    :param question: Câu hỏi người dùng.
    :type question: str
    :param chat_history: Lịch sử trò chuyện trước đây.

        Danh sách lịch sử theo dạng: `[{type: user|agent, message: str}]`
    
    :type chat_history: list[dict]
    :return: Câu hỏi đã được chuẩn hóa.
    :rtype: str
    """
    
    if chat_history is None:
        chat_history = []
    
    processed_question = None
    
    
    # ====== TODO: Thực hiện cài đặt dưới đây ======
    # Nếu không có lịch sử chat, trả về câu hỏi gốc
    if not chat_history:
        processed_question = question
    else:
        # Xây dựng chuỗi lịch sử chat
        history_text = ""
        for msg in chat_history:
            msg_type = msg.get('type', 'user')
            msg_content = msg.get('message', '')
            if msg_type == 'user':
                history_text += f"Người dùng: {msg_content}\n"
            else:
                history_text += f"Trợ lý: {msg_content}\n"
        
        # Tạo prompt để chuẩn hóa câu hỏi dựa trên lịch sử
        prompt_template = ChatPromptTemplate(
            [
                ("system", IDENTITY_PROMPT),
                ("system", """
Bạn là một trợ lý hỗ trợ chuẩn hóa câu hỏi từ người dùng.

Nhiệm vụ của bạn là chuyển đổi câu hỏi của người dùng thành một câu hỏi độc lập, rõ ràng và đầy đủ dựa trên lịch sử cuộc trò chuyện.

Hướng dẫn:
- Nếu câu hỏi có đại từ (như "nó", "họ", "đó", "này") hoặc tham chiếu đến ngữ cảnh trước đó, hãy thay thế chúng bằng thông tin cụ thể từ lịch sử.
- Nếu câu hỏi đã rõ ràng và không cần ngữ cảnh, giữ nguyên câu hỏi.
- Chỉ trả về câu hỏi đã được chuẩn hóa, không thêm bất kỳ giải thích hay bình luận nào.
- Câu hỏi chuẩn hóa phải hoàn chỉnh, dễ hiểu và có thể đứng độc lập mà không cần lịch sử trò chuyện.
                """),
                ("human", """
Lịch sử trò chuyện:
{history}

Câu hỏi hiện tại: {question}

Câu hỏi đã chuẩn hóa:
                """)
            ],
            input_variables=["history", "question"]
        )
        
        processed_question = llm_chat_base.generate(
            prompt=prompt_template.format_messages(history=history_text, question=question)
        )
    
    
    # ====== Hết phần cài đặt ======
    
    assert "Kết quả trả về phải là str", isinstance(processed_question, str)
    
    return processed_question