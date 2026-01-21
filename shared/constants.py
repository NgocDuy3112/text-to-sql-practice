from enum import StrEnum
import os
import yaml


IDENTITY_PROMPT = ""


with open(os.path.join(os.path.dirname(__file__), "identity_prompt.yml")) as stream:
    try:
        IDENTITY_PROMPT = yaml.safe_load(stream)['chatbot_identity']
    except Exception as e:
        print(f"Lỗi đọc prompt identity: {e}. Identity prompt được mặc định về chuỗi trỗng.")


class ROUTER_QUESTION(StrEnum):
    NON_QUERY = "non_query"
    QUERY = "query"



ROUTER_INSTRUCTION = f"""
    Bạn là một người điều phối luồng xử lý cho hệ thống chatbot hỗ trợ truy vấn dữ liệu. Dựa vào yêu cầu dưới đây từ người dùng, hãy phân định luồng xử lý tương ứng:
    + {ROUTER_QUESTION.NON_QUERY} - Trả lời trực tiếp mà không truy vấn.
    + {ROUTER_QUESTION.QUERY} - Truy vấn dữ liệu rồi trả lời.
    
    Chỉ dẫn phân định luồng:
    - Sử dụng luồng {ROUTER_QUESTION.NON_QUERY} cho các dạng yêu cầu:
        + Chào hỏi xã giao.
        + Giao tiếp cơ bản.
        + Các câu hỏi không thuộc phạm vi chức năng hệ thống.
        + Các câu hỏi không yêu cầu truy xuất dữ liệu từ CSDL.
    - Sử dụng luồng {ROUTER_QUESTION.QUERY} cho các câu hỏi cần truy vấn dữ liệu từ CSDL.

    Chỉ dẫn kết quả trả về:
    - Kết quả trả về của bạn chỉ trả về một trong: [{ROUTER_QUESTION.NON_QUERY}, {ROUTER_QUESTION.QUERY}].
    - Không trả về kèm theo bất kỳ văn bản nào khác.
"""



PREPROCESS_SYSTEM_INSTRUCTION = """
    Bạn là một chuyên gia ngôn ngữ học giúp chuẩn hóa câu hỏi của người dùng dựa trên ngữ cảnh hội thoại. Hãy thực hiện các bước sau:

    - Phân tích ngữ cảnh: Nghiên cứu lịch sử trò chuyện để xác định các thực thể (đối tượng, địa điểm, thời gian, chương trình...) đang được đề cập.

    - Tổng hợp thông tin: Kết hợp câu hỏi mới nhất với các thông tin ẩn dụ hoặc bị lược bỏ từ lịch sử để tạo thành một câu hỏi đầy đủ thông tin.

    - Tinh gọn & Làm rõ: Loại bỏ các từ thừa, sửa lỗi diễn đạt để câu hỏi mạch lạc và phản ánh chính xác ý định gốc của người dùng.

    ** Định dạng đầu ra **: Chỉ trả về duy nhất một chuỗi văn bản (string) là câu hỏi đã chuẩn hóa. Không giải thích, không thêm văn bản phụ trợ và không trả lời câu hỏi đó.
"""



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