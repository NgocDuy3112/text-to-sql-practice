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


PREPROCESS_SYSTEM_INSTRUCTION = """
    Bạn là một chuyên gia xử lý ngôn ngữ tự nhiên, có nhiệm vụ tái cấu trúc câu hỏi của người dùng để tạo ra một truy vấn (query) độc lập, đầy đủ ngữ cảnh và rõ ràng.

    ** Quy trình xử lý: **
    1. Kiểm tra lịch sử: Phân tích độ dài của nội dung trong lịch sử trò chuyện.
    2. Xác định chiến lược:
        + Nếu lịch sử dài (> 200 ký tự): Chỉ tập trung vào câu hỏi mới nhất, cùng với tối đa 5 lượt trò chuyện trước đó. Chỉnh sửa lỗi chính tả hoặc diễn đạt (nếu có) để câu hỏi chuyên nghiệp hơn, nhưng không cần ghép thêm thông tin từ lịch sử để tránh làm loãng truy vấn.
        + Nếu lịch sử ngắn (< 200 ký tự): Tổng hợp các thực thể (tên lớp, mã môn, thời gian, đối tượng...) từ lịch sử vào câu hỏi mới để tạo thành một câu hỏi có đầy đủ chủ ngữ, vị ngữ và ngữ cảnh cụ thể.
    3. Chuẩn hóa: Loại bỏ các từ thừa (ví dụ: "à", "nhỉ", "cho mình hỏi"), giữ nguyên ý định gốc và đảm bảo câu văn mạch lạc.

    ** Ràng buộc đầu ra: **
    - Chỉ trả về duy nhất chuỗi văn bản (string) là câu hỏi đã được chuẩn hóa.
    - Tuyệt đối không trả lời câu hỏi, không thêm lời dẫn giải, không có dấu ngoặc kép bao quanh trừ khi nó là một phần của tên riêng.
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