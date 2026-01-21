def preprocess_question(question: str, chat_history: list[dict] = []) -> str:
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
    
    processed_question = None
    
    
    # ====== TODO: Thực hiện cài đặt dưới đây ======
    
    
    
    # ====== Hết phần cài đặt ======
    
    assert "Kết quả trả về phải là str", isinstance(processed_question, str)
    
    return processed_question