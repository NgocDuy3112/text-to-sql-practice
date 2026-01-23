"""
Tester cho phần thực hành 05 - Truy vấn tương đồng mô tả bảng.
Chạy tester:
    + Tại thư mục dự án.
    + Chạy lệnh `python -m tests.T05_context_retriever`.
"""

from implements.P05_context_retriever import retrieve_context
from tests.test_data import RETRIEVER_DATA



def main():
    total = 0
    total_matched = 0
    details = []

    for idx, data in enumerate(RETRIEVER_DATA):
        question = data.get('question', "")
        table_lst = data.get('table_name', [])
        context_table = retrieve_context(question)
        predicted_names = [t.name for t in context_table]

        # Đánh giá: số lượng bảng đúng
        matched = len(set(table_lst) & set(predicted_names))
        percent = matched / len(table_lst) if table_lst else 0
        total += len(table_lst)
        total_matched += matched

        details.append({
            'idx': idx + 1,
            'question': question,
            'groundtruth': table_lst,
            'predicted': predicted_names,
            'matched': matched,
            'percent': percent
        })

    # Thống kê tổng quát
    overall_percent = total_matched / total if total else 0
    print(f"\n>>> Thống kê tổng quát <<<")
    print(f"Tỉ lệ xác định đúng: {overall_percent:.2%}")

    print(f"\n>>> Chi tiết từng điểm dữ liệu <<<")
    for d in details:
        print(f"\n--- Dữ liệu {d['idx']} ---")
        print(f"Câu hỏi: {d['question']}")
        print(f"Bảng cần truy vấn: {d['groundtruth']}")
        print(f"Kết quả trả về: {d['predicted']}")
        print(f"Số bảng đúng: {d['matched']} / {len(d['groundtruth'])} ({d['percent']:.2%})")



if __name__ == "__main__":
    main()