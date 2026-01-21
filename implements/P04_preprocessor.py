from langchain_core.prompts import ChatPromptTemplate
from shared.constants import IDENTITY_PROMPT, PREPROCESS_SYSTEM_INSTRUCTION
from shared.messages import ChatbotMessage
from shared.chat_model import llm_chat_base


def preprocess_question(question: str, chat_history: list[ChatbotMessage] = []) -> str:
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
    
    # ====== TODO: Thực hiện cài đặt dưới đây ======

    # Chuẩn hóa lịch sử trò chuyện thành chuỗi để đưa vào system prompt
    history_str = ""
    if chat_history:
        history_items: list[str] = []
        for message in chat_history:
            chat_message = f'{message.type}: {message.content}'
            history_items.append(chat_message)
        history_str = "\n".join(history_items)

    prompt_template = ChatPromptTemplate(
        [
            ("system", PREPROCESS_SYSTEM_INSTRUCTION),
            ("human", """
                **Dữ liệu đầu vào:**
                - Lịch sử trò chuyện: {chat_history}
                - Tin nhắn mới: {question}
            """),
        ],
        input_variables=["chat_history", "question"],
    )

    messages = prompt_template.format_messages(chat_history=history_str, question=question)
    processed_question = llm_chat_base.generate(messages)

    # ====== Hết phần cài đặt ======

    assert isinstance(processed_question, str), "Kết quả trả về phải là str"

    return processed_question