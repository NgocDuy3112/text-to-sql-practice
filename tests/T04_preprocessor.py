"""
Tester cho phần thực hành 04 - Tiền xử lý yêu cầu người dùng.
Chạy tester:
    + Tại thư mục dự án.
    + Chạy lệnh `python -m tests.T04_preprocessor`.
"""

import json
from implements.P04_preprocessor import preprocess_question
from tests.test_data import PREPROCESSOR_DATA
from shared.messages import ChatbotMessage


def _process_data(data: dict):    
    new_ques = data.get('new_message', "")
    chat_hist = []
    
    for hist in data.get('chat_history', []):
        msg = ChatbotMessage.from_data(hist)
        chat_hist.append(msg)
    
    return new_ques, chat_hist

def main():
    output = []
    
    for data in PREPROCESSOR_DATA:
        new_question, chat_history = _process_data(data)
        processed_question = preprocess_question(new_question, chat_history)
        
        ques_type = data.get('type', "")
        ques_note = data.get('note', "")
        
        output.append(
            {
                'question': data.get('new_message', ""),
                'chat_history': data.get('chat_history', []),
                'output': processed_question,
                'sample': data.get('sample_normalized_query', ""),
                'type': f"{ques_type} - {ques_note}"
            }
        )

    print("\n>>> Thành phần cho kết quả <<<")
    for o in output:
        hist_str = json.dumps(o['chat_history'], ensure_ascii=False)
        
        print(f"\n> Loại hình câu hỏi: {o['type']}")
        print(f"  Lịch sử: {hist_str}")
        print(f"  Câu hỏi: {o['question']}")
        print(f"  Mẫu kết quả: {o['sample']}")
        print(f"  > Kết quả thật: {o['output']}")


if __name__ == "__main__":
    main()