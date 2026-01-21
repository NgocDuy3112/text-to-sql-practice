import os
import yaml


IDENTITY_PROMPT = ""


with open(os.path.join(os.path.dirname(__file__), "identity_prompt.yml")) as stream:
    try:
        IDENTITY_PROMPT = yaml.safe_load(stream)['chatbot_identity']
    except Exception as e:
        print(f"Lỗi đọc prompt identity: {e}. Identity prompt được mặc định về chuỗi trỗng.")



NON_QUERY_SAMPLES = [
    "Xin chào",
    "Tôi có thể hỏi bạn điều gì?",
    "Bạn tên là gì?",
    "Bạn có thể giúp gì cho tôi?",
    "Hướng dẫn sử dụng chatbot này như thế nào?"
]



QUERY_SAMPLES = [
    "Cho tôi biết lớp học này có tối đa bao nhiêu học viên?",
    "Lập bảng điểm của lớp LP02",
    "Hiện nay đội ngũ giảng viên có bao nhiêu người?",
    "Lớp LP02 dạy về kiến thức nào?",
    "Lập bảng điểm tổng kết của anh X, số điện thoại 0123456987"
]