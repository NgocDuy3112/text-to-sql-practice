from implements import ROUTER_QUESTION

ROUTER_DATA = [
    {"question": "Xin chào", "expected": ROUTER_QUESTION.NON_QUERY},
    {"question": "Hi", "expected": ROUTER_QUESTION.NON_QUERY},
    {"question": "Bạn là ai", "expected": ROUTER_QUESTION.NON_QUERY},
    {"question": "Chatbot này dùng dữ liệu gì", "expected": ROUTER_QUESTION.NON_QUERY},
    {"question": "Bạn có thể làm những gì", "expected": ROUTER_QUESTION.NON_QUERY},
    {"question": "Hướng dẫn tôi cách đặt câu hỏi", "expected": ROUTER_QUESTION.NON_QUERY},
    {"question": "Chào bạn, tôi cần hỗ trợ.", "expected": ROUTER_QUESTION.NON_QUERY},
    {"question": "Bạn có thể giúp gì cho tôi?", "expected": ROUTER_QUESTION.NON_QUERY},
    {"question": "Bạn có thể giúp tôi truy vấn những thông tin nào?", "expected": ROUTER_QUESTION.NON_QUERY},
    {"question": "Tôi có thể yêu cầu bạn làm gì?", "expected": ROUTER_QUESTION.NON_QUERY},
    {"question": "Lập danh sách các dữ liệu tôi truy vấn được?", "expected": ROUTER_QUESTION.NON_QUERY},
    {"question": "Hiện có bao nhiêu học viên", "expected": ROUTER_QUESTION.QUERY},
    {"question": "Danh sách các chương trình học hiện có", "expected": ROUTER_QUESTION.QUERY},
    {"question": "Mỗi chương trình có học phí bao nhiêu", "expected": ROUTER_QUESTION.QUERY},
    {"question": "Có bao nhiêu lớp học đang mở", "expected": ROUTER_QUESTION.QUERY},
    {"question": "Những lớp nào đang diễn ra trong tháng 3", "expected": ROUTER_QUESTION.QUERY},
    {"question": "Tổng số giảng viên hiện tại là bao nhiêu?", "expected": ROUTER_QUESTION.QUERY},
    {"question": "Liệt kê các khóa học đang mở?", "expected": ROUTER_QUESTION.QUERY},
    {"question": "Học phí của lớp lập trình cơ bản là bao nhiêu?", "expected": ROUTER_QUESTION.QUERY},
    {"question": "Hiện tại có bao nhiêu lớp đang tạm dừng?", "expected": ROUTER_QUESTION.QUERY},
    {"question": "Những lớp lập trình cơ bản khi nào mở tiếp?", "expected": ROUTER_QUESTION.QUERY},
]


PREPROCESSOR_DATA = [
    {
      "type": "Câu hỏi đơn",
      "chat_history": [
        { "role": "user", "content": "Xin chào" },
        { "role": "assistant", "content": "Chào bạn, tôi có thể giúp gì?" }
      ],
      "new_message": "Hiện có bao nhiêu chương trình học",
      "sample_normalized_query": "Hiện có bao nhiêu chương trình học",
      "note": "Lịch sử không liên quan, bỏ qua"
    },
    {
      "type": "Câu hỏi đơn",
      "chat_history": [
        { "role": "user", "content": "Bạn là ai" },
        { "role": "assistant", "content": "Tôi là chatbot hỗ trợ khai thác dữ liệu đào tạo" }
      ],
      "new_message": "Danh sách các lớp học hiện có",
      "sample_normalized_query": "Danh sách các lớp học hiện có",
      "note": "Lịch sử không liên quan, bỏ qua"
    },
    {
      "type": "Câu hỏi đơn",
      "chat_history": [
        { "role": "user", "content": "Chương trình lập trình cơ bản hiện có mấy lớp" },
        { "role": "assistant", "content": "Chương trình lập trình cơ bản hiện có 5 lớp" },
        { "role": "user", "content": "Tổng học viên của cả 5 lớp là bao nhiêu" },
        { "role": "assistant", "content": "Tổng học viên của 5 lớp lập trình cơ bản là 30" },
      ],
      "new_message": "Tìm điểm cuối khóa lớp lập trình nâng cao của Nguyễn Văn Anh, sinh 2000",
      "sample_normalized_query": "Tìm điểm cuối khóa lớp lập trình nâng cao của Nguyễn Văn Anh sinh năm 2000",
      "note": "Lịch sử không liên quan, bỏ qua"
    },
    {
      "type": "Câu hỏi tiếp nối",
      "chat_history": [
        { "role": "user", "content": "Lớp VP01 thuộc chương trình nào" },
        { "role": "assistant", "content": "Lớp VP01 thuộc chương trình Tin học văn phòng cơ bản" }
      ],
      "new_message": "Lớp đó có bao nhiêu học viên",
      "sample_normalized_query": "Lớp VP01 có bao nhiêu học viên",
      "note": "Tham chiếu thực thể trong lịch sử"
    },
    {
      "type": "Câu hỏi tiếp nối",
      "chat_history": [
        { "role": "user", "content": "Chương trình Python cơ bản có học phí bao nhiêu" },
        { "role": "assistant", "content": "Học phí là 2.500.000 đồng" }
      ],
      "new_message": "Chương trình đó học bao lâu",
      "sample_normalized_query": "Chương trình Python cơ bản học bao lâu",
      "note": "Tham chiếu thực thể trong lịch sử"
    },
    {
      "type": "Câu hỏi tiếp nối",
      "chat_history": [
        { "role": "user", "content": "Ai là giảng viên chính của lớp PY01" },
        { "role": "assistant", "content": "Giảng viên chính là Lê Thanh Sơn" },
        { "role": "user", "content": "Lớp này có bao nhiêu học viên" },
        { "role": "assistant", "content": "Lớp PY01 có 20 học viên." },
      ],
      "new_message": "Những học viên đó có điểm cuối khóa chưa",
      "sample_normalized_query": "Những học viên của lớp PY01 có điểm cuối khóa chưa",
      "note": "Tham chiếu thực thể trong lịch sử"
    },
    {
      "type": "Câu hỏi tiếp nối",
      "chat_history": [
        { "role": "user", "content": "Lớp VP01 thuộc chương trình nào" },
        { "role": "assistant", "content": "Lớp VP01 thuộc chương trình Tin học văn phòng cơ bản" }
      ],
      "new_message": "Cho tôi biết lịch học của lớp đó",
      "sample_normalized_query": "Cho tôi biết thời khoá biểu của lớp VP01",
      "note": "Tham chiếu thực thể trong lịch sử"
    },
]

RETRIEVER_DATA = [
  {
    "question": "Hiện có bao nhiêu chương trình đào tạo?",
    "table_name": ["chuong_trinh"]
  },
  {
    "question": "Danh sách các lớp học thuộc chương trình 'Lập trình Python cơ bản'.",
    "table_name": ["lop_hoc", "chuong_trinh"]
  },
  {
    "question": "Mỗi lớp học hiện có bao nhiêu học viên đăng ký?",
    "table_name": ["lop_hoc", "dang_ky_lop"]
  },
  {
    "question": "Danh sách học viên đang học lớp có mã 'LH3'.",
    "table_name": ["hoc_vien", "dang_ky_lop"]
  },
  {
    "question": "Điểm cuối khóa của học viên Nguyễn Văn An ở lớp 'VP01'.",
    "table_name": ["hoc_vien", "lop_hoc", "diem_cuoi_khoa"]
  },
  {
    "question": "Danh sách giảng viên phụ trách lớp 'PY01' và vai trò của họ.",
    "table_name": ["giang_vien", "giang_vien_phu_trach", "lop_hoc"]
  },
  {
    "question": "Những lớp học nào đang diễn ra trong tháng 3 năm 2025?",
    "table_name": ["lop_hoc"]
  },
  {
    "question": "Mỗi giảng viên hiện đang tham gia giảng dạy bao nhiêu lớp?",
    "table_name": ["giang_vien", "giang_vien_phu_trach"]
  },
  {
    "question": "Danh sách các lớp học mà học viên có email an.nguyen@example.com đã đăng ký.",
    "table_name": ["hoc_vien", "dang_ky_lop", "lop_hoc"]
  },
  {
    "question": "Tổng số học viên đang học trong mỗi chương trình đào tạo.",
    "table_name": ["chuong_trinh", "lop_hoc", "dang_ky_lop"]
  }
]